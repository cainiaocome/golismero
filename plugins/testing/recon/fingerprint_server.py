#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__="""
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

from golismero.api.config import Config
from golismero.api.data.resource.domamin import *
from golismero.api.logger import Logger
from golismero.api.net.protocol import NetworkAPI
from golismero.api.net.web_utils import is_in_scope
from golismero.api.plugin import TestingPlugin
from golismero.api.text.wordlist_api import WordListAPI


class SuspiciousURLPlugin(TestingPlugin):
    """
    Find suspicious words in URLs.
    """


    #----------------------------------------------------------------------
    def check_input_params(self, inputParams):
        pass


    #----------------------------------------------------------------------
    def display_help(self):
        # TODO: this could default to the description found in the metadata.
        return self.__doc__


    #----------------------------------------------------------------------
    def get_accepted_info(self):
        return [Url.RESOURCE_URL]


    #----------------------------------------------------------------------
    def recv_info(self, info):

        if not isinstance(info, D):
            raise TypeError("Expected Url, got %s instead" % type(info))

        m_url = info.url

        # Check if URL is in scope
        if not is_in_scope(m_url):
            return

        # Load wordlists
        m_wordlist = WordListAPI().get_wordlist(Config.plugin_config['wordlist'])

        # Return matching keywords
        return [SuspiciousURL(info, x)
                for x in m_wordlist
                if x in m_url]
