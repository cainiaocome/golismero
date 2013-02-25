#!/usr/bin/env python
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

__all__ = ["Url"]

from .information import Information


#------------------------------------------------------------------------------
class Url(Information):
	"""
	URL results.
	"""


	#----------------------------------------------------------------------
	def __init__(self, url, method = "GET", url_params = None, post_params= None, content_type = None, request_type = 0):
		"""
		Construct a URL result.

		:param url: URL to manage
		:type url: str

		:param method: HTTP method to get URL
		:type method: str

		:param url_params: params inside URL
		:type url_params: dict

		:param post_params: params inside post
		:type post_params: dict
		"""
		super(Url, self).__init__()
		self.result_subtype = self.INFORMATION_URL

		# URL
		self.__url = url

		# Method
		self.__method = 'GET' if not method else method.upper()

		# Params in URL
		self.__url_params = url_params if url_params else {}

		# Params as post
		self.__post_params = post_params if post_params else {}

		# HTTPs?
		self.__is_https = url.lower().startswith("https://")

		# Content type
		self.__content_type = content_type

		# Request type
		self.__request_type = request_type



	#----------------------------------------------------------------------
	def __str__(self):
		return "[%s] %s (%s)" % (
			self.__method,
			self.__url,
			''.join(["%s = %s | " % (k, v) for k, v in (self.__url_params.items() if self.__method != 'POST' else self.__post_params.items())])[:-2]
		)


	#----------------------------------------------------------------------
	@property
	def url(self):
		"""
		str -- Raw URL
		"""
		return self.__url

	@property
	def method(self):
		"""
		str -- HTTP method
		"""
		return self.__method

	@property
	def url_params(self):
		"""
		dict(str) -- URL parameters
		"""
		return self.__url_params

	@property
	def post_params(self):
		"""
		dict(str) -- POST parameters
		"""
		return self.__post_params

	@property
	def is_https(self):
		"""
		bool -- True if it's HTTPS, False otherwise
		"""
		return self.__is_https

	@property
	def has_url_param(self):
		"""
		bool - True if there are URL params, False otherwise
		"""
		return bool(self.url_params)

	@property
	def has_post_param(self):
		"""
		bool - True if there are POST params, False otherwise
		"""
		return bool(self.post_params)

	@property
	def content_type(self):
		"""
		str - MIME content type
		"""
		return self.__content_type

	@property
	def request_type(self):
		"""
		int - One of the HTML.TYPE_* constants
		"""
		return self.__request_type
