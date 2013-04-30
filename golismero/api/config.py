#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------
# Plugin configuration API
#-----------------------------------------------------------------------

__license__="""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

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

__all__ = ["Config"]

from ..common import Singleton

class _Config (Singleton):
    """
    Current plugin configuration.

    Whenever a plugin accesses this object it will receive its own
    configuration, including the current audit's name and settings.
    """

    @property
    def audit_name(self):
        "str -- Name of the audit."
        return self.__context.audit_name

    @property
    def audit_config(self):
        "AuditConfig -- Parameters of the audit."
        return self.__context.audit_config

    @property
    def plugin_info(self):
        "PluginInfo -- Plugin information."
        return self.__context.plugin_info

    @property
    def plugin_name(self):
        "str -- Plugin name."
        return self.plugin_info.plugin_name

    @property
    def plugin_module(self):
        "str -- Module where the plugin was loaded from."
        return self.plugin_info.plugin_module

    @property
    def plugin_class(self):
        "str -- Class name of the plugin."
        return self.plugin_info.plugin_class

    @property
    def plugin_config(self):
        "dict(str -> str) -- Plugin configuration."
        return self.plugin_info.plugin_config

    @property
    def plugin_extra_config(self):
        "dict(dict(str -> str)) -- Plugin extra configuration."
        return self.plugin_info.plugin_extra_config

    # The following properties may only be used internally.

    @property
    def _context(self):
        ":returns: PluginContext"
        return self.__context

    @_context.setter
    def _context(self, context):
        ":type context: PluginContext"
        # TODO: check the call stack to make sure it's called only
        #       from pre-approved places.
        self.__context = context

Config = _Config()
