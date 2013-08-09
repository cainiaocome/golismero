#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from golismero.api.audit import get_audit_count, get_audit_names, \
     get_audit_info, start_audit, stop_audit
from golismero.api.config import Config
from golismero.api.logger import Logger
from golismero.api.plugin import UIPlugin, get_plugin_info
from golismero.messaging.codes import MessageType, MessageCode

import multiprocessing
import time
import threading
import warnings


#------------------------------------------------------------------------------
class WebUIPlugin(UIPlugin):
    """
    Web UI plugin.
    """


    #--------------------------------------------------------------------------
    def get_accepted_info(self):
        "This method tells the Orchestrator we don't want to receive any Data."
        return []


    #--------------------------------------------------------------------------
    def recv_info(self, info):
        "This method won't be called, because we don't receive any Data."
        pass


    #--------------------------------------------------------------------------
    def recv_msg(self, message):
        """
        This method receives messages from the Orchestrator, parses them, and
        calls the appropriate notification methods defined below.

        :param message: Message received from the Orchestrator.
        :type message: Message
        """

        # Control messages.
        if message.message_type == MessageType.MSG_TYPE_CONTROL:

            # This UI plugin must be started.
            if message.message_code == MessageCode.MSG_CONTROL_START_UI:
                self.start_ui()

            # This UI plugin must be shut down.
            elif message.message_code == MessageCode.MSG_CONTROL_STOP_UI:
                self.stop_ui()

            # An audit has started.
            elif message.message_code == MessageCode.MSG_CONTROL_START_AUDIT:
                self.notify_stage(message.audit_name, "start")

            # An audit has finished.
            elif message.message_code == MessageCode.MSG_CONTROL_STOP_AUDIT:
                self.notify_stage(message.audit_name,
                    "finish" if message.message_info else "cancel")

            # A plugin has sent a log message.
            elif message.message_code == MessageCode.MSG_CONTROL_LOG:
                plugin_name = self.get_plugin_name(message)
                (text, level, is_error) = message.message_info
                if is_error:
                    self.notify_error(message.audit_name, plugin_name, text, level)
                else:
                    self.notify_log(message.audit_name, plugin_name, text, level)

            # A plugin has sent an error message.
            elif message.message_code == MessageCode.MSG_CONTROL_ERROR:
                plugin_name = self.get_plugin_name(message)
                (description, traceback) = message.message_info
                text = "Error: " + description
                self.notify_error(message.audit_name, plugin_name, text, Logger.STANDARD)
                text = "Exception raised: %s\n%s" % (description, traceback)
                self.notify_error(message.audit_name, plugin_name, text, Logger.MORE_VERBOSE)

            # A plugin has sent a warning message.
            elif message.message_code == MessageCode.MSG_CONTROL_WARNING:
                plugin_name = self.get_plugin_name(message)
                for w in message.message_info:
                    formatted = warnings.formatwarning(w.message, w.category, w.filename, w.lineno, w.line)
                    text = "Warning: " + w.message
                    self.notify_warning(message.audit_name, plugin_name, text, Logger.STANDARD)
                    text = "Warning details: " + formatted
                    self.notify_warning(message.audit_name, plugin_name, text, Logger.MORE_VERBOSE)

        # Status messages.
        elif message.message_type == MessageType.MSG_TYPE_STATUS:

            # A plugin has started processing a Data object.
            if message.message_type == MessageCode.MSG_STATUS_PLUGIN_BEGIN:
                plugin_name = self.get_plugin_name(message)
                self.notify_progress(message.audit_name, plugin_name, message.message_info, 0.0)

            # A plugin has finished processing a Data object.
            elif message.message_type == MessageCode.MSG_STATUS_PLUGIN_END:
                plugin_name = self.get_plugin_name(message)
                self.notify_progress(message.audit_name, plugin_name, message.message_info, 100.0)

            # A plugin is currently processing a Data object.
            elif message.message_code == MessageCode.MSG_STATUS_PLUGIN_STEP:
                plugin_name = self.get_plugin_name(message)
                identity, progress = message.message_info
                self.notify_progress(message.audit_name, plugin_name, identity, progress)

            # An audit has switched to another execution stage.
            elif message.message_code == MessageCode.MSG_STATUS_STAGE_UPDATE:
                self.notify_stage(message.audit_name, message.message_info)


    #--------------------------------------------------------------------------
    @staticmethod
    def get_plugin_name(message):
        """
        Helper method to get a user-friendly name
        for the plugin that sent a given message.

        :param message: Message sent by a plugin.
        :type message: Message

        :returns: User-friendly name for the plugin.
        :rtype: str
        """
        if message.plugin_name:
            plugin_info = get_plugin_info(message.plugin_name)
            if plugin_info:
                return plugin_info.display_name
        return "GoLismero"


    #--------------------------------------------------------------------------
    def start_ui(self):
        """
        This method is called when the UI start message arrives.
        It reads the plugin configuration, starts the consumer thread, and
        launches the Django web application.
        """

        # Get the configuration.
        bind_address = Config.plugin_config.get("bind_address", "127.0.0.1")
        bind_port    = int( Config.plugin_config.get("bind_port", "8080") )

        # Create the consumer thread object.
        self.thread_stop = False
        self.thread = threading.Thread(target = self.consumer_thread)
        self.thread.daemon = True

        # Create the duplex pipe to talk to the Django application.
        self.parent_conn, self.child_conn = multiprocessing.Pipe(duplex=True)

        #
        # TODO
        #
        raise NotImplementedError("Plugin under construction!")

        # Start the consumer thread.
        self.thread.start()


    #--------------------------------------------------------------------------
    def stop_ui(self):
        """
        This method is called when the UI stop message arrives.
        It shuts down the web UI.
        """

        # Tell the consumer thread to stop.
        self.thread_stop = False

        # Shut down the communication pipe.
        # This should wake up the consumer thread.
        try:
            self.parent_conn.close()
        except:
            pass
        try:
            self.child_conn.close()
        except:
            pass

        # Wait for the consumer thread to stop.
        if self.thread.isAlive():
            self.thread.join(2.0)

        # If a timeout occurs...
        if self.thread.isAlive():

            # Forcefully kill the thread. Ignore errors.
            # http://stackoverflow.com/a/15274929/426293
            import ctypes
            exc = ctypes.py_object(KeyboardInterrupt)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self.thread.ident), exc)
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(self.thread.ident), None)

        #
        # TODO
        #


    #--------------------------------------------------------------------------
    def consumer_thread(self):
        """
        This method implements the consumer thread code: it reads data sent by
        the Django application though a pipe, and sends the appropriate
        messages to the Orchestrator.
        """
        #
        # TODO
        #
        pass


    #--------------------------------------------------------------------------
    def notify_log(self, audit_name, plugin_name, text, level):
        """
        This method is called when a plugin sends a log message.

        :param audit_name: Name of the audit.
        :type audit_name: str

        :param plugin_name: Name of the plugin.
        :type plugin_name: str

        :param text: Log text.
        :type text: str

        :param level: Log level (0 through 3).
        :type level: int
        """
        packet = ("log", audit_name, plugin_name, text, level)
        self.child_conn.send(packet)


    #--------------------------------------------------------------------------
    def notify_error(self, audit_name, plugin_name, text, level):
        """
        This method is called when a plugin sends an error message.

        :param audit_name: Name of the audit.
        :type audit_name: str

        :param plugin_name: Name of the plugin.
        :type plugin_name: str

        :param text: Log text.
        :type text: str

        :param level: Log level (0 through 3).
        :type level: int
        """
        packet = ("error", audit_name, plugin_name, text, level)
        self.child_conn.send(packet)


    #--------------------------------------------------------------------------
    def notify_warning(self, audit_name, plugin_name, text, level):
        """
        This method is called when a plugin sends a warning message.

        :param audit_name: Name of the audit.
        :type audit_name: str

        :param plugin_name: Name of the plugin.
        :type plugin_name: str

        :param text: Log text.
        :type text: str

        :param level: Log level (0 through 3).
        :type level: int
        """
        packet = ("warn", audit_name, plugin_name, text, level)
        self.child_conn.send(packet)


    #--------------------------------------------------------------------------
    def notify_progress(self, audit_name, plugin_name, identity, progress):
        """
        This method is called when a plugin sends a status update.

        :param audit_name: Name of the audit.
        :type audit_name: str

        :param plugin_name: Name of the plugin.
        :type plugin_name: str

        :param identity: Identity hash of the Data object being processed.
        :type identity: str

        :param progress: Progress percentage (0.0 through 100.0).
        :type progress: float
        """
        packet = ("progress", audit_name, plugin_name, identity, progress)
        self.child_conn.send(packet)


    #--------------------------------------------------------------------------
    def notify_stage(self, audit_name, stage):
        """
        This method is called when an audit moves to another execution stage.

        :param audit_name: Name of the audit.
        :type audit_name: str

        :param stage: Name of the execution stage.
            Must be one of the following:
             - "start" - The audit has just started.
             - "import" - Importing external data into the database.
             - "recon" - Performing reconnaisance on the targets.
             - "scan" - Scanning the targets for vulnerabilities.
             - "attack" - Attacking the target using the vulnerabilities found.
             - "intrude" - Gathering information after a successful attack.
             - "cleanup" - Cleaning up after an attack.
             - "report" - Generating a report for the audit.
             - "finish" - The audit has finished.
             - "cancel" - The audit has been canceled by the user.
        :type stage: str
        """
        packet = ("stage", audit_name, stage)
        self.child_conn.send(packet)
