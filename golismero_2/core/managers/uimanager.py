#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Author: Daniel Garcia Garcia a.k.a cr0hn | dani@iniqua.com

Golismero project site: http://code.google.com/p/golismero/
Golismero project mail: golismero.project@gmail.com

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

from core.managers.priscillapluginmanager import PriscillaPluginManager
from core.messaging.notifier import UINotifier
from core.messaging.message import Message
from core.main.commonstructures import Singleton, GlobalParams, IReceiver
from threading import Thread
from time import sleep

#------------------------------------------------------------------------------
class UIManager(Singleton, Thread, IReceiver):
    """
    This class manage the UI managers.
    """

    #----------------------------------------------------------------------
<<<<<<< HEAD:golismero_2/core/managers/uimanager.py
    def __init__(self, config, orchestrator):
=======
    def __vinit__(self):
        """Virtual contructor. Initialize common vars."""
        self.__receiver = None
        self.__notifier = None

    #----------------------------------------------------------------------
    def set_config(self, params, orchestrator):
>>>>>>> d246c4c20dab744ef5b779e54446f25d6709dda7:golismero_2/core/main/uimanager.py
        """
        Constructor

        :param config: Configuration for module
        :type config: GlobalParams

        :param orchestrator: orchestrator instance
        :type orchestrator: Orchestrator
        """
<<<<<<< HEAD:golismero_2/core/managers/uimanager.py

        # For singleton pattern
        if self._is_instanced:
            return


        # Init and start notifier
        self.__notifier = UINotifier()
        self.__notifier.start()

        # Set configs
        self.__receiver = orchestrator
        self.__params = config
=======

        if not isinstance(params, GlobalParams):
            raise TypeError("Expected GlobalParams, got %s instead" % type(params))
        #if not isinstance(orchestrator, Orchestrator):
            #raise TypeError("Expected Orchestrator, got %s instead" % type(orchestrator))

        self.__params = params
        self.__receiver = orchestrator

    #----------------------------------------------------------------------
    def start(self):
        """Start UI specified by params."""

        if not self.__receiver or not self.__params:
            raise RuntimeError("Orchestrator not initialized")
>>>>>>> d246c4c20dab744ef5b779e54446f25d6709dda7:golismero_2/core/main/uimanager.py

        #
        # Start UI system
        #
        m_plugins = None

        # 1 - Get UI plugin, by params
        if self.__params.USER_INTERFACE.console is GlobalParams.USER_INTERFACE.console:
            # Add console UI plugins to nofitier
            m_plugins =  PriscillaPluginManager().get_all_plugins("ui")
        else:
            m_plugins =  PriscillaPluginManager().get_all_plugins("ui")

        # 2 - Configure plugins to be it own the target of messages and add
        #     to notifier
        for p in m_plugins.values():
            p.set_observer(self)
            self.__notifier.add_plugin(p)


    #----------------------------------------------------------------------
<<<<<<< HEAD:golismero_2/core/managers/uimanager.py
    def run(self):
        """Stop or break UI"""
=======
    def stop_ui(self):
        """Stop or break UI."""
>>>>>>> d246c4c20dab744ef5b779e54446f25d6709dda7:golismero_2/core/main/uimanager.py
        if self.__notifier.is_finished:
            #self.shutdown()
            sleep(0.025)

    #----------------------------------------------------------------------
    def recv_msg(self, message):
        """
        Send message info to UI plugins.

        :param message: The message unencapsulate to get info.
        :type message: Message
        """
        if isinstance(message, Message):
<<<<<<< HEAD:golismero_2/core/managers/uimanager.py
            self.__notifier.nofity(message)

    #----------------------------------------------------------------------
    def __get_is_finished(self):
        """
        If UI has finished return True. False otherwise.

        :returns: True, if finished. False otherwise.
        """
        return self.__notifier.is_finished
    is_finished = property(__get_is_finished)

    #----------------------------------------------------------------------
    def stop(self):
        """
        Stop UI plugins
        """
        self.__notifier.stop()
=======
            self.__notifier.notify(message)
>>>>>>> d246c4c20dab744ef5b779e54446f25d6709dda7:golismero_2/core/main/uimanager.py
