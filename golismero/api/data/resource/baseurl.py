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

__all__ = ["BaseUrl"]

from ..data import identity
from .resource import Resource
from ...net.web_utils import DecomposedURL


#------------------------------------------------------------------------------
class BaseUrl(Resource):
    """
    Base URL information type.
    """

    resource_type = Resource.RESOURCE_BASE_URL


    #----------------------------------------------------------------------
    def __init__(self, url):
        """
        Base URL information type.

        :param url: Any URL. The base will be extracted from it.
        :type url: str
        """
        assert isinstance(url, basestring)

        # Parse, verify and canonicalize the URL.
        parsed = DecomposedURL(url)
        if not parsed.host or not parsed.scheme:
            raise ValueError("Only absolute URLs must be used!")

        # Convert it into a base URL.
        parsed.auth = None
        parsed.path = "/"
        parsed.fragment = None
        parsed.query = None
        parsed.query_char = None
        url = parsed.url

        # Raw base URL.
        self.__url = url

        # Parsed base URL.
        self.__parsed_url = parsed

        # Parent constructor.
        super(BaseUrl, self).__init__()


    #----------------------------------------------------------------------
    def __str__(self):
        return self.url


    #----------------------------------------------------------------------
    def __repr__(self):
        return "<BaseUrl url=%r>" % self.url


    #----------------------------------------------------------------------
    @identity
    def url(self):
        """
        str -- Raw URL.
        """
        return self.__url


    #----------------------------------------------------------------------
    @property
    def parsed_url(self):
        """
        DecomposedURL -- Parsed URL.
        """
        return self.__parsed_url


    #----------------------------------------------------------------------
    @property
    def is_https(self):
        """
        bool -- True if it's HTTPS, False otherwise.
        """
        return self.__parsed.scheme == "https"