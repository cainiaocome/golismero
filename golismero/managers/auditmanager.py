#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manager for audits.
"""

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/cr0hn/golismero/
Golismero project mail: golismero.project<@>gmail.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

__all__ = ["AuditManager", "Audit"]

from ..api.data import Data
from ..api.data.resource import Resource
from ..api.data.resource.url import Url
from ..api.config import Config
from ..common import AuditConfig
from ..scope import AuditScope
from ..database.auditdb import AuditDB
from ..managers.importmanager import ImportManager
from ..managers.processmanager import PluginContext
from ..managers.reportmanager import ReportManager
from ..messaging.codes import MessageType, MessageCode, MessagePriority
from ..messaging.message import Message
from ..messaging.notifier import AuditNotifier

from datetime import datetime
from os import getpid
from warnings import catch_warnings, warn


#--------------------------------------------------------------------------
class AuditManager (object):
    """
    Manage and control audits.
    """

    #----------------------------------------------------------------------
    def __init__(self, orchestrator, config):
        """
        :param orchestrator: Core to send messages to.
        :type orchestrator: Orchestrator

        :param config: Global configuration object.
        :type config: OrchestratorConfig
        """

        # Create the dictionary where we'll store the Audit objects.
        self.__audits = dict()

        # Keep a reference to the Orchestrator.
        self.__orchestrator = orchestrator


    #----------------------------------------------------------------------
    @property
    def orchestrator(self):
        """
        :returns: Orchestrator instance.
        :rtype: Orchestrator
        """
        return self.__orchestrator


    #----------------------------------------------------------------------
    def new_audit(self, audit_config):
        """
        Creates a new audit.

        :param audit_config: Parameters of the audit.
        :type audit_config: AuditConfig

        :returns: Newly created audit.
        :rtype: Audit
        """
        if not isinstance(audit_config, AuditConfig):
            raise TypeError("Expected AuditConfig, got %r instead" % type(audit_config))

        # Create the audit.
        m_audit = Audit(audit_config, self.orchestrator)

        # Store it.
        self.__audits[m_audit.name] = m_audit

        # Run!
        m_audit.run()

        # Return it.
        return m_audit


    #----------------------------------------------------------------------
    def has_audits(self):
        """
        Determine if there are audits currently runnning.

        :returns: True if there are audits in progress, False otherwise.
        :rtype: bool
        """
        return bool(self.__audits)


    #----------------------------------------------------------------------
    def get_all_audits(self):
        """
        Get the currently running audits.

        :returns: Mapping of audit names to instances.
        :rtype: dict(str -> Audit)
        """
        return self.__audits


    #----------------------------------------------------------------------
    def get_audit(self, name):
        """
        Get an instance of an audit by its name.

        :param name: Audit name.
        :type name: str

        :returns: Audit instance.
        :rtype: Audit

        :raises KeyError: No audit exists with that name.
        """
        return self.__audits[name]


    #----------------------------------------------------------------------
    def remove_audit(self, name):
        """
        Delete an instance of an audit by its name.

        :param name: Audit name.
        :type name: str

        :raises KeyError: No audit exists with that name.
        """
        try:
            self.orchestrator.netManager.release_all_slots(name)
        finally:
            try:
                audit = self.__audits[name]
                try:
                    audit.close()
                finally:
                    del self.__audits[name]
            finally:
                self.orchestrator.cacheManager.clean(name)


    #----------------------------------------------------------------------
    def dispatch_msg(self, message):
        """
        Process an incoming message from the Orchestrator.

        :param message: Incoming message.
        :type message: Message

        :returns: True if the message was sent, False if it was dropped.
        :rtype: bool
        """
        if not isinstance(message, Message):
            raise TypeError("Expected Message, got %s instead" % type(message))

        # Send info messages to their target audit
        if message.message_type == MessageType.MSG_TYPE_DATA:
            if not message.audit_name:
                raise ValueError("Info message with no target audit!")
            return self.get_audit(message.audit_name).dispatch_msg(message)

        # Process control messages
        elif message.message_type == MessageType.MSG_TYPE_CONTROL:

            # Send ACKs to their target audit
            if message.message_code == MessageCode.MSG_CONTROL_ACK:
                if message.audit_name:
                    audit = self.get_audit(message.audit_name)
                    audit.acknowledge(message)

            # Stop an audit if requested
            elif message.message_code == MessageCode.MSG_CONTROL_STOP_AUDIT:
                if not message.audit_name:
                    raise ValueError("I don't know which audit to stop...")
                self.get_audit(message.audit_name).close()
                self.remove_audit(message.audit_name)

            # TODO: pause and resume audits, start new audits

        return True


    #----------------------------------------------------------------------
    def close(self):
        """
        Release all resources held by all audits.
        """
        for name in self.__audits.keys(): # not iterkeys, will be modified
            try:
                self.remove_audit(name)
            except:
                pass


#--------------------------------------------------------------------------
class Audit (object):
    """
    Instance of an audit, with its custom parameters, scope, target, plugins, etc.
    """


    #----------------------------------------------------------------------
    def __init__(self, audit_config, orchestrator):
        """
        :param orchestrator: Orchestrator instance that will receive messages sent by this audit.
        :type orchestrator: Orchestrator

        :param auditParams: Audit configuration.
        :type auditParams: AuditConfig
        """

        if not isinstance(audit_config, AuditConfig):
            raise TypeError("Expected AuditConfig, got %s instead" % type(audit_config))

        # Keep the audit settings.
        self.__audit_config = audit_config

        # Keep a reference to the Orchestrator.
        self.__orchestrator = orchestrator

        # Set the audit name.
        self.__name = self.__audit_config.audit_name
        if not self.__name:
            self.__name = self.generate_audit_name()
            self.__audit_config.audit_name = self.__name

        # Set the current stage to the first stage.
        self.__current_stage = orchestrator.pluginManager.min_stage

        # Initialize the "report started" flag.
        self.__is_report_started = False

        # Maximum number of links to follow.
        self.__followed_links = 0
        self.__show_max_links_warning = True

        # Number of unacknowledged messages.
        self.__expecting_ack = 0

        # Initialize the managers to None.
        self.__notifier = None
        self.__import_manager = None
        self.__report_manager = None
        self.__database = None


    #----------------------------------------------------------------------

    @property
    def name(self):
        """
        :returns: Name of the audit.
        :rtype: str
        """
        return self.__name

    @property
    def orchestrator(self):
        """
        :returns: Orchestrator instance that will receive messages sent by this audit.
        :rtype: Orchestrator
        """
        return self.__orchestrator

    @property
    def config(self):
        """
        :returns: Audit configuration.
        :rtype: AuditConfig
        """
        return self.__audit_config

    @property
    def scope(self):
        """
        :returns: Audit scope.
        :rtype: AuditScope
        """
        return self.__audit_scope

    @property
    def database(self):
        """
        :returns: Audit database.
        :rtype: AuditDB
        """
        return self.__database

    @property
    def importManager(self):
        """
        :returns: Import manager.
        :rtype: ImportManager
        """
        return self.__import_manager

    @property
    def reportManager(self):
        """
        :returns: Report manager.
        :rtype: ReportManager
        """
        return self.__report_manager


    #----------------------------------------------------------------------

    @property
    def expecting_ack(self):
        """
        :returns: Number of ACKs expected by this audit.
        :rtype: int
        """
        return self.__expecting_ack

    @property
    def current_stage(self):
        """
        :returns: Current execution stage.
        :rtype: str
        """
        return self.__current_stage

    @property
    def is_report_started(self):
        """
        :returns: True if report generation has started, False otherwise.
        :rtype: bool
        """
        return self.__is_report_started


    #----------------------------------------------------------------------
    @staticmethod
    def generate_audit_name():
        """
        Generate a default name for a new audit.

        :returns: Generated name.
        :rtype: str
        """
        return "golismero-" + datetime.now().strftime("%Y-%m-%d-%H_%M_%S")


    #----------------------------------------------------------------------
    def run(self):
        """
        Start execution of an audit.
        """

        # Reset the number of unacknowledged messages.
        self.__expecting_ack = 0

        # Keep the original execution context.
        old_context = Config._context

        try:

            # Update the execution context for this audit.
            Config._context = PluginContext(getpid(), old_context.msg_queue,
                                            audit_name   = self.name,
                                            audit_config = self.config)

            # Calculate the audit scope.
            # This is done here because some DNS queries may be made.
            self.__audit_scope = AuditScope(self.config)

            # Update the execution context again, with the scope.
            Config._context = PluginContext(getpid(), old_context.msg_queue,
                                            audit_name   = self.name,
                                            audit_config = self.config,
                                            audit_scope  = self.scope)

            # Find the plugins.
            success, failure = self.orchestrator.pluginManager.find_plugins(
                self.orchestrator.config.plugins_folder)
            if not success:
                raise RuntimeError("Failed to find any plugins!")

            # Apply the plugin black and white lists.
            self.orchestrator.pluginManager.apply_black_and_white_lists(
                self.config.enabled_plugins, self.config.disabled_plugins)

            # Calculate the plugin dependencies.
            self.orchestrator.pluginManager.calculate_dependencies()

            # Create the notifier.
            self.__notifier = AuditNotifier(self)

            # Load the testing plugins.
            m_audit_plugins = self.orchestrator.pluginManager.load_plugins("testing")

            # Register the testing plugins with the notifier.
            self.__notifier.add_multiple_plugins(m_audit_plugins)

            # Create the import manager.
            self.__import_manager = ImportManager(self.config, self.orchestrator)

            # Create the report manager.
            self.__report_manager = ReportManager(self.config, self.orchestrator)

            # Create the database.
            self.__database = AuditDB(self.name, self.config.audit_db)

            # Add the targets to the database, but only if they're new.
            # (Makes sense when resuming a stopped audit).
            target_data = self.scope.get_targets()
            for data in target_data:
                if self.database.has_data_key(data.identity, data.data_type):
                    self.database.add(data)

            # Import external results.
            # This is done after storing the targets, so the importers
            # can overwrite the targets with new information if available.
            self.importManager.import_results()

        finally:

            # Restore the original execution context.
            Config._context = old_context

##        # Move to the next stage.
##        self.update_stage()

        # XXX HACK
        # Temporarily doing this because update_stage is broken.
        self.send_msg(message_info=target_data)


    #----------------------------------------------------------------------
    def send_info(self, data):
        """
        Send data to the Orchestrator.

        :param data: Data to send.
        :type data: Data
        """
        return self.send_msg(message_type = MessageType.MSG_TYPE_DATA,
                             message_info = [data])


    #----------------------------------------------------------------------
    def send_msg(self, message_type = MessageType.MSG_TYPE_DATA,
                       message_code = MessageCode.MSG_DATA,
                       message_info = None,
                       priority = MessagePriority.MSG_PRIORITY_MEDIUM):
        """
        Send messages to the Orchestrator.

        :param message_type: Message type. Must be one of the constants from MessageType.
        :type mesage_type: int

        :param message_code: Message code. Must be one of the constants from MessageCode.
        :type message_code: int

        :param message_info: The payload of the message. Its type depends on the message type and code.
        :type message_info: *

        :param priority: Priority level. Must be one of the constants from MessagePriority.
        :type priority: int
        """
        m = Message(message_type = message_type,
                    message_code = message_code,
                    message_info = message_info,
                      audit_name = self.name,
                        priority = priority)
        self.orchestrator.enqueue_msg(m)


    #----------------------------------------------------------------------
    def acknowledge(self, message):
        """
        Got an ACK for a message sent from this audit to the plugins.

        :param message: The message with the ACK.
        :type message: Message
        """
        try:

            # Decrease the expected ACK count.
            # The audit manager will check when this reaches zero.
            self.__expecting_ack -= 1

            # Tell the notifier about this ACK.
            self.__notifier.acknowledge(message)

        finally:

            # Check for audit stage termination.
            #
            # NOTE: This check assumes messages always arrive in order,
            #       and ACKs are always sent AFTER responses from plugins.
            #
            if not self.expecting_ack:

                # Update the current stage.
                self.update_stage()


    #----------------------------------------------------------------------
    def update_stage(self):
        """
        Sets the current stage to the minimum needed to process pending data.
        When the last stage is completed, sends the audit stop message.
        """

        # If the reports are finished...
        if self.__is_report_started:

            # Send the audit end message.
            self.send_msg(message_type = MessageType.MSG_TYPE_CONTROL,
                          message_code = MessageCode.MSG_CONTROL_STOP_AUDIT,
                          message_info = True)   # True for finished, False for user cancel

        # If the reports are not yet launched...
        else:

            # Get the database and the plugin manager.
            database = self.database
            pluginManager = self.orchestrator.pluginManager

            # Look for the earliest stage with pending data.
            for stage in xrange(pluginManager.min_stage, pluginManager.max_stage + 1):
                self.__current_stage = stage
                pending = database.get_pending_data(stage)
                if pending:

                    # Get the pending data.
                    # XXX FIXME possible performance problem here!
                    datalist = map(database.get_data, pending)

                    # If we don't have any suitable plugins...
                    if not self.__notifier.is_runnable_stage(datalist, stage):

                        # Mark all data as having finished this stage.
                        for identity in pending:
                            database.mark_stage_finished(identity, stage)

                        # Skip to the next stage.
                        continue

                    # Send the pending data to the Orchestrator.
                    self.send_msg(
                        message_type = MessageType.MSG_TYPE_DATA,
                        message_info = datalist,
                    )

                    # We're done, return.
                    return

            # If we reached this point, we finished the last stage.
            # Launch the report generation.
            self.__current_stage = pluginManager.max_stage + 1
            self.generate_reports()


    #----------------------------------------------------------------------
    def dispatch_msg(self, message):
        """
        Send messages to the plugins of this audit.

        :param message: The message to send.
        :type message: Message

        :returns: True if the message was sent, False if it was dropped.
        :rtype: bool
        """
        if not isinstance(message, Message):
            raise TypeError("Expected Message, got %s instead" % type(message))

        # Keep the original execution context.
        old_context = Config._context

        try:

            # Update the execution context for this audit.
            Config._context = PluginContext(getpid(), old_context.msg_queue,
                                            audit_name   = self.name,
                                            audit_config = self.config,
                                            audit_scope  = self.scope)

            # Dispatch the message.
            return self.__dispatch_msg(message)

        finally:

            # Restore the original execution context.
            Config._context = old_context

    def __dispatch_msg(self, message):

        # Get the database and the plugin manager.
        database = self.database
        pluginManager = self.orchestrator.pluginManager

        # Is it data?
        if message.message_type == MessageType.MSG_TYPE_DATA:

            # Here we'll store the data to be resent to the plugins.
            data_for_plugins = []

            # For each data object sent...
            if isinstance(message.message_info, Data):
                message.message_info = [message.message_info]
            for data in message.message_info:

                # Check the type.
                if not isinstance(data, Data):
                    warn("TypeError: Expected Data, got %r instead" % type(data), RuntimeWarning)
                    continue

                # Is the data new?
                if not database.has_data_key(data.identity):

                    # Increase the number of links followed.
                    if data.data_type == Data.TYPE_RESOURCE and data.resource_type == Resource.RESOURCE_URL:
                        self.__followed_links += 1

                        # Maximum number of links reached?
                        if self.__audit_config.max_links > 0 and self.__followed_links >= self.__audit_config.max_links:

                            # Show a warning, but only once.
                            if self.__show_max_links_warning:
                                self.__show_max_links_warning = False
                                w = "Maximum number of links (%d) reached! Audit: %s"
                                w = w % (self.__audit_config.max_links, self.name)
                                with catch_warnings(record=True) as wlist:
                                    warn(w, RuntimeWarning)
                                self.send_msg(message_type = MessageType.MSG_TYPE_CONTROL,
                                              message_code = MessageCode.MSG_CONTROL_WARNING,
                                              message_info = wlist,
                                              priority = MessagePriority.MSG_PRIORITY_HIGH)

                            # Skip this data object.
                            continue

                # Add the data to the database.
                # This automatically merges the data if it already exists.
                database.add_data(data)

                # If the data is in scope...
                if data.is_in_scope():

                    # If the plugin is not recursive, mark the data as already processed by it.
                    plugin_name = message.plugin_name
                    if plugin_name:
                        plugin_info = pluginManager.get_plugin_by_name(plugin_name)
                        if plugin_info.recursive:
                            database.mark_plugin_finished(data.identity, plugin_name)

                    # The data will be sent to the plugins.
                    data_for_plugins.append(data)

                # If the data is NOT in scope...
                else:

                    # Mark the data as having completed all stages.
                    database.mark_stage_finished(data.identity, pluginManager.max_stage)

            # Recursively process newly discovered data, if any.
            # Discovered data already in the database is ignored.
            visited = {data.identity for data in data_for_plugins}  # Skip original data.
            for data in list(data_for_plugins):  # Can't iterate and modify!
                queue = list(data.discovered)    # Make sure it's a copy.
                while queue:
                    data = queue.pop(0)
                    if (data.identity not in visited and
                        not database.has_data_key(data.identity)
                    ):
                        database.add_data(data)       # No merging because it's new.
                        visited.add(data.identity)    # Prevents infinite loop.
                        queue.extend(data.discovered) # Recursive.
                        if data.is_in_scope():        # If in scope, send it to plugins.
                            data_for_plugins.append(data)
                        else:                         # If not, mark as completed.
                            database.mark_stage_finished(data.identity, pluginManager.max_stage)

            # If we have data to be sent...
            if data_for_plugins:

                # Modify the message in-place with the filtered list of data objects.
                message._update_data(data_for_plugins)

                # Send the message to the plugins, and track the expected ACKs.
                self.__expecting_ack += self.__notifier.notify(message)

                # Tell the Orchestrator we sent the message.
                return True

        # Tell the Orchestrator we dropped the message.
        return False


    #----------------------------------------------------------------------
    def generate_reports(self):
        """
        Start the generation of reports for the audit.
        """

        # Check if the report generation is already started.
        if self.__is_report_started:
            raise RuntimeError("Why are you asking for the report twice?")

        # An ACK is expected after launching the report plugins.
        self.__expecting_ack += 1
        try:

            # Mark the report generation as started for this audit.
            self.__is_report_started = True

            # Start the report generation.
            self.__expecting_ack += self.__report_manager.generate_reports(self.__notifier)

        # Send the ACK after launching the report plugins.
        finally:
            self.send_msg(message_type = MessageType.MSG_TYPE_CONTROL,
                          message_code = MessageCode.MSG_CONTROL_ACK,
                              priority = MessagePriority.MSG_PRIORITY_LOW)


    #----------------------------------------------------------------------
    def close(self):
        """
        Release all resources held by this audit.
        """
        try:
            self.database.compact()
        finally:
            self.database.close()
