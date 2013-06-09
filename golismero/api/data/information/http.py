#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HTTP requests and responses.
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

__all__ = ["HTTP_Request", "HTTP_Response"]

from . import Information
from .html import HTML
from .. import identity
from ...net.web_utils import DecomposedURL

import re
import httplib
import mimetools


#------------------------------------------------------------------------------
class HTTP_Headers (object):
    """
    HTTP headers.

    Unlike other methods of storing HTTP headers in Python this class preserves
    the original order of the headers, doesn't remove duplicated headers,
    preserves the original case but still letting your access them in a
    case-insensitive manner, and is read-only.

    Also see: :ref:`parse_headers`
    """

    # Also see: https://en.wikipedia.org/wiki/List_of_HTTP_header_fields


    #----------------------------------------------------------------------
    def __init__(self, raw_headers):
        """
        :param raw_headers: Raw headers to parse.
        :type raw_headers: str
        """
        self.__raw_headers = raw_headers
        self.__headers, self.__cache = self.parse_headers(raw_headers)


    #----------------------------------------------------------------------
    @staticmethod
    def from_items(items):
        """
        Get HTTP headers in pre-parsed form.

        This is useful for integrating with other libraries that have
        already parsed the HTTP headers in their own way.

        :param items: Iterable of key/value pairs.
        :type items: iterable( tuple(str, str) )
        """

        # Reconstruct the raw headers the best we can.
        reconstructed = [
            "%s: %s" % (name,
                        (value if value.endswith("\r\n") else value + "\r\n")
                        )
            for name, value in items
        ]
        reconstructed.append("\r\n")
        raw_headers = "".join(reconstructed)

        # Return an HTTP_Headers object using the reconstructed raw headers.
        return HTTP_Headers(raw_headers)


    #----------------------------------------------------------------------
    @staticmethod
    def parse_headers(raw_headers):
        """
        Parse HTTP headers.

        Unlike other common Python solutions (mimetools, etc.) this one
        properly supports multiline HTTP headers and duplicated header
        merging as specified in the RFC.

        The parsed headers are returned in two forms.

        The first is an n-tuple of 2-tuples of strings containing each
        header's name and value. The original case and order is preserved,
        as well as any whitespace and line breaks in the values. Duplicate
        headers are not merged or dealt with in any special way. This aims
        at preserving the headers in original form as much as possible
        without resorting to the raw headers themselves, for example for
        fingerprint analysis of the web server.

        The second is a dictionary mapping header names to their values.
        Duplicate headers are merged as per RFC specs, and multiline headers
        are converted to single line headers to avoid line breaks in the
        values. Header names are converted to lowercase for easier case
        insensitive lookups. This aims at making it easier to get the values
        of the headers themselves rather than analyzing the web server.

        :param raw_headers: Raw headers to parse.
        :type raw_headers: str

        :returns: Parsed headers in original and simplified forms.
        :rtype: tuple( tuple(tuple(str, str)), dict(str -> str) )
        """

        # Split the headers into lines and parse each line.
        original = []
        parsed = {}
        last_name = None
        for line in raw_headers.split("\r\n"):

            # If we find an empty line, stop processing.
            if not line:
                break

            # If the line begins with whitespace, it's a continuation.
            if line[0] in " \t":
                if last_name is None:
                    break                              # broken headers
                line = line.strip()
                parsed[last_name] += " " + line
                item = original[-1]
                item = (item[0], item[1] + " " + line)
                original[-1] = item
                continue                               # next line

            # Split the name and value pairs.
            name, value = line.split(":", 1)

            # Strip the leading and trailing whitespace.
            name  = name.strip()
            value = value.strip()

            # Convert the name to lowercase.
            name_lower = name.lower()

            # Remember the last name we've seen.
            last_name = name_lower

            # Add the headers to the parsed form.
            # If the name already exists, merge the headers.
            # If not, add a new one.
            if name_lower in parsed:
                parsed[name_lower] += ", " + value
            else:
                parsed[name_lower] = value

            # Add the headers to the original form.
            original.append( (name, value) )

        # Convert the original headers list into a tuple to make it
        # read-only, then return the tuple and the dictionary.
        return tuple(original), parsed


    #----------------------------------------------------------------------
    def __str__(self):
        return self.__raw_headers


    #----------------------------------------------------------------------
    def __repr__(self):
        return "<%s headers=%r>" % (self.__class__.__name__, self.__headers)


    #----------------------------------------------------------------------
    def to_tuple(self):
        """
        Convert the headers to Python tuples of strings.

        :returns: Headers.
        :rtype: tuple( tuple(str, str) )
        """

        # Immutable object, we can return it directly.
        return self.__headers


    #----------------------------------------------------------------------
    def to_dict(self):
        """
        Convert the headers to a Python dictionary.

        :returns: Headers.
        :rtype: dict(str -> str)
        """

        # Mutable object, we need to make a copy.
        # It can be a shallow copy because it only contains strings.
        return self.__cache.copy()


    #----------------------------------------------------------------------
    def __iter__(self):
        """
        When iterated, whole header lines are returned.
        To iterate header names and values use iterkeys(), itervalues()
        or iteritems().

        :returns: Iterator of header lines.
        :rtype: iter(str)
        """
        return ("%s: %s\r\n" % item for item in self.__headers)


    #----------------------------------------------------------------------
    def iteritems(self):
        """
        When iterating, the original case and order of the headers
        is preserved. This means some headers may be repeated.

        :returns: Iterator of header names and values.
        :rtype: iter( tuple(str, str) )
        """
        return self.__headers.__iter__()


    #----------------------------------------------------------------------
    def iterkeys(self):
        """
        When iterating, the original case and order of the headers
        is preserved. This means some headers may be repeated.

        :returns: Iterator of header names.
        :rtype: iter(str)
        """
        return (name for name, _ in self.__headers)


    #----------------------------------------------------------------------
    def itervalues(self):
        """
        When iterating, the original case and order of the headers
        is preserved. This means some headers may be repeated.

        :returns: Iterator of header values.
        :rtype: iter(str)
        """
        return (value for _, value in self.__headers)


    #----------------------------------------------------------------------
    def __getitem__(self, key):
        """
        The [] operator works both for index lookups and key lookups.

        When provided with an index, the whole header line is returned.

        When provided with a header name, the value is looked up.
        Only the first header of that name is returned. Comparisons
        are case-insensitive.

        :param key: Index or header name.
        :type key: int | str

        :returns: Header line (for indices) or value (for names).
        :rtype: str
        """
        if type(key) in (int, long):
            return "%s: %s\r\n" % self.__headers[key]
        try:
            key = key.lower()
        except AttributeError:
            raise TypeError("Expected str, got %s" % type(key))
        return self.__cache[key]


    #----------------------------------------------------------------------
    def get(self, name, default = None):
        """
        Get a header by name.

        Comparisons are case-insensitive. When more than one header has
        the requested name, only the first one is returned.

        :param name: Header name.
        :type name: str

        :returns: Header value.
        :rtype: str
        """
        try:
            name = name.lower()
        except AttributeError:
            raise TypeError("Expected str, got %s" % type(name))
        try:
            return self.__cache[name]
        except KeyError:
            return default


    #----------------------------------------------------------------------
    def __getslice__(self, start = None, end = None):
        """
        When sliced, whole header lines are returned in a single string.

        :param start: Start of the slice.
        :type start: int | None

        :param end: End of the slice.
        :type end: int | None

        :returns: The requested header lines merged into a single string.
        :rtype: str
        """
        return "".join("%s: %s\r\n" % item for item in self.__headers[start:end])


#------------------------------------------------------------------------------
class HTTP_Request (Information):
    """
    HTTP request information.
    """

    information_type = Information.INFORMATION_HTTP_REQUEST


    #
    # TODO:
    #   Parse and reconstruct requests as it's done with responses.
    #   It may be useful one day, for example, for HTTP proxying.
    #


    # Default headers to use in HTTP requests.
    DEFAULT_HEADERS = (
        ("User-Agent", "Mozilla/5.0 (compatible, GoLismero/2.0 The Web Knife; +https://github.com/cr0hn/golismero)"),
        ("Accept-Language", "en-US"),
        ("Accept", "*/*"),
        ("Cache-Control", "no-store"),
        ("Pragma", "no-cache"),
        ("Expires", "0"),
    )


    #----------------------------------------------------------------------
    def __init__(self, url, headers = None, post_data = None, method = "GET", protocol = "HTTP", version = "1.1"):
        """
        :param url: Absolute URL to connect to.
        :type url: str

        :param headers: HTTP headers, in raw or parsed form. Defaults to DEFAULT_HEADERS.
        :type headers: HTTP_Headers | dict(str -> str) | tuple( tuple(str, str) ) | str

        :param post_data: POST data.
        :type post_data: str | None

        :param method: HTTP method.
        :type method: str

        :param protocol: Protocol name.
        :type protocol: str

        :param version: Protocol version.
        :type version: str
        """

        # HTTP method.
        self.__method = method.upper()

        # URL.
        self.__parsed_url = DecomposedURL(url)
        self.__url = self.__parsed_url.url

        # HTTP headers.
        if headers is None:
            headers = self.DEFAULT_HEADERS
            if version == "1.1":
                headers = ("Host", self.__parsed_url.host) + headers
            headers = HTTP_Headers.from_items(headers)
        elif not isinstance(headers, HTTP_Headers):
            if type(headers) == unicode:
                headers = str(headers)   # FIXME: better collation!
            if type(headers) == str:             # raw headers
                headers = HTTP_Headers(headers)
            elif hasattr(headers, "items"):      # dictionary
                headers = HTTP_Headers.from_items(sorted(headers.items()))
            else:                                # dictionary items
                headers = HTTP_Headers.from_items(sorted(headers))
        self.__headers = headers

        # POST data.
        self.__post_data = post_data

        # Call the parent constructor.
        super(HTTP_Request, self).__init__()


    #----------------------------------------------------------------------

    @identity
    def method(self):
        """
        :returns: HTTP method.
        :rtype: str
        """
        return self.__method

    @identity
    def url(self):
        """
        :returns: URL.
        :rtype: str
        """
        return self.__url

    @identity
    def protocol(self):
        """
        :returns: Protocol name.
        :rtype: str
        """
        return self.__protocol

    @identity
    def version(self):
        """
        :returns: Protocol version.
        :rtype: str
        """
        return self.__version

    @identity
    def headers(self):
        """
        :return: HTTP headers.
        :rtype: HTTP_Headers
        """
        return self.__headers

    @identity
    def post_data(self):
        """
        :return: POST data.
        :rtype: str | None
        """
        return self.__post_data


    #----------------------------------------------------------------------

    @property
    def parsed_url(self):
        """
        :returns: URL split to its components.
        :rtype: DecomposedURL
        """
        return self.__parsed_url

    @property
    def request_uri(self):
        """
        :return: Request URI.
        :rtype: str
        """
        return self.__parsed_url.request_uri

    @property
    def hostname(self):
        """
        :return: 'Host' HTTP header.
        :rtype: str
        """
        return self.__headers.get('Host')

    @property
    def user_agent(self):
        """
        :return: 'User-Agent' HTTP header.
        :rtype: str
        """
        return self.__headers.get('User-Agent')

    @property
    def accept_language(self):
        """
        :return: 'Accept-Language' HTTP header.
        :rtype: str
        """
        return self.__headers.get('Accept-Language')

    @property
    def accept(self):
        """
        :return: 'Accept' HTTP header.
        :rtype: str
        """
        return self.__headers.get('Accept')

    @property
    def referer(self):
        """
        :return: 'Referer' HTTP header.
        :rtype: str
        """
        return self.__headers.get('Referer')

    @property
    def cookie(self):
        """
        :return: 'Cookie' HTTP header.
        :rtype: str
        """
        return self.__headers.get('Cookie')

    @property
    def content_type(self):
        """
        :return: 'Content-Type' HTTP header.
        :rtype: str
        """
        return self.__headers.get('Content-Type')

    @property
    def content_length(self):
        """
        :return: 'Content-Length' HTTP header.
        :rtype: int
        """
        return int(self.__headers.get('Content-Length'))


#------------------------------------------------------------------------------
class HTTP_Response (Information):
    """
    HTTP response information.
    """

    information_type = Information.INFORMATION_HTTP_RESPONSE


    #----------------------------------------------------------------------
    def __init__(self, request, **kwargs):
        """
        All optional arguments must be passed as keywords.

        :param request: HTTP request that originated this response.
        :type request: HTTP_Request

        :param raw_response: (Optional) Raw bytes received from the server.
        :type raw_response: str

        :param status: (Optional) HTTP status code. Defaults to "200".
        :type status: str

        :param reason: (Optional) HTTP reason message.
        :type reason: str

        :param protocol: (Optional) Protocol name. Defaults to "HTTP".
        :type protocol: str

        :param version: (Optional) Protocol version. Defaults to "1.1".
        :type version: str

        :param raw_headers: (Optional) Raw HTTP headers.
        :type raw_headers: str

        :param headers: (Optional) Parsed HTTP headers.
        :type headers: HTTP_Headers | dict(str -> str) | tuple( tuple(str, str) )

        :param data: (Optional) Raw data that followed the response headers.
        :type data: str
        """

        # Initialize everything.
        self.__raw_response = None
        self.__raw_headers  = None
        self.__status       = "200"
        self.__reason       = None
        self.__protocol     = "HTTP"
        self.__version      = "1.1"
        self.__headers      = None
        self.__data         = None

        # Raw response bytes.
        self.__raw_response = kwargs.get("raw_response", None)
        if self.__raw_response:
            self.__parse_raw_response(request)

        # Status line.
        self.__status   = kwargs.get("status",   self.__status)
        self.__reason   = kwargs.get("reason",   self.__reason)
        self.__protocol = kwargs.get("protocol", self.__protocol)
        self.__version  = kwargs.get("version",  self.__version)
        if self.__status and not self.__reason:
            try:
                self.__reason = httplib.responses[self.__status]
            except Exception:
                pass
        elif not self.__status and self.__reason:
            lower_reason = self.__reason.strip().lower()
            for code, text in httplib.responses.iteritems():
                if text.lower() == lower_reason:
                    self.__status = str(code)
                    break

        # HTTP headers.
        self.__raw_headers = kwargs.get("raw_headers", self.__raw_headers)
        self.__headers = kwargs.get("headers", self.__headers)
        if self.__headers:
            if not isinstance(self.__headers, HTTP_Headers):
                if hasattr(headers, "items"):
                    self.__headers = HTTP_Headers(sorted(self.__headers.items()))
                else:
                    self.__headers = HTTP_Headers(sorted(self.__headers))
            if not self.__raw_headers:
                self.__reconstruct_raw_headers()
        elif self.__raw_headers and not self.__headers:
            self.__parse_raw_headers()

        # Data.
        self.__data = kwargs.get("data",  self.__data)

        # Reconstruct the raw response if needed.
        if not self.__raw_response:
            self.__reconstruct_raw_response()

        # Call the parent constructor.
        super(HTTP_Response, self).__init__()

        # Link this response to the request that originated it.
        self.add_link(request)


    #----------------------------------------------------------------------

    @identity
    def raw_response(self):
        """
        :returns: Raw HTTP response.
        :rtype: str | None
        """
        return self.__raw_response


    #----------------------------------------------------------------------

    @property
    def status(self):
        """
        :returns: HTTP status code.
        :rtype: str | None
        """
        return self.__status

    @property
    def reason(self):
        """
        :returns: HTTP reason message.
        :rtype: str | None
        """
        return self.__reason

    @property
    def protocol(self):
        """
        :returns: Protocol name.
        :rtype: str | None
        """
        return self.__protocol

    @property
    def version(self):
        """
        :returns: Protocol version.
        :rtype: str | None
        """
        return self.__version

    @property
    def headers(self):
        """
        :return: HTTP headers.
        :rtype: dict(str -> str) | None
        """
        return self.__headers

    @property
    def raw_headers(self):
        """
        :returns: HTTP method used for this request.
        :rtype: str | None
        """
        return self.__raw_headers

    @property
    def data(self):
        """
        :return: Response data.
        :rtype: str | None
        """
        return self.__data

    @property
    def content_length(self):
        """
        :return: 'Content-Length' HTTP header.
        :rtype: int | None
        """
        if self.__headers:
            return int(self.__headers.get('Content-Length'))

    @property
    def content_disposition(self):
        """
        :return: 'Content-Disposition' HTTP header.
        :rtype: str | None
        """
        if self.__headers:
            return self.__headers.get('Content-Disposition')

    @property
    def transport_encoding(self):
        """
        :return: 'Transport-Encoding' HTTP header.
        :rtype: str | None
        """
        if self.__headers:
            return self.__headers.get('Transport-Encoding')

    @property
    def cookie(self):
        """
        :return: 'Set-Cookie' HTTP header.
        :rtype: str | None
        """
        if self.__headers:
            return self.__headers.get('Set-Cookie')

    set_cookie = cookie

    @property
    def server(self):
        """
        :return: 'Server' HTTP header.
        :rtype: str | None
        """
        if self.__headers:
            return self.__headers.get('Server')


    #----------------------------------------------------------------------
    def __parse_raw_response(self, request):

        # Special case: if parsing HTTP/0.9, everything is data.
        if request.version == "0.9":
            self.__protocol = "HTTP"
            self.__version  = "0.9"
            self.__status   = "200"
            self.__reason   = httplib.responses[200]
            self.__data     = self.__raw_response
            return

        # Split the response from the data.
        response, data = self.__raw_response.split("\r\n\r\n", 1)
        response = response + "\r\n\r\n"

        # Split the response line from the headers.
        raw_line, raw_headers = response.split("\r\n", 1)

        # Split the response line into its components.
        try:
            proto_version, status, reason = re.split("[ \t]+", raw_line, 2)
        except Exception:
            proto_version, status = re.split("[ \t]+", raw_line, 1)
            try:
                reason = httplib.responses[int(status)]
            except Exception:
                reason = None
        if "/" in proto_version:
            protocol, version = proto_version.split("/")
        else:
            protocol = proto_version
            version  = None

        # Set missing components to None.
        if not status:
            status = None
        if not reason:
            reason = None
        if not protocol:
            protocol = None
        if not data:
            data = None

        # Store the components.
        self.__protocol    = protocol
        self.__version     = version
        self.__status      = status
        self.__reason      = reason
        self.__raw_headers = raw_headers
        self.__data        = data

        # Parse the raw headers.
        self.__parse_raw_headers()


    #----------------------------------------------------------------------
    def __reconstruct_raw_response(self):

        # Special case: if parsing HTTP/0.9, everything is data.
        if self.__version == "0.9":
            self.__raw_response = self.__data
            return

        # FIXME: not sure how Requests handles content encoding,
        # it may be possible to generate broken raw responses if
        # the content is decoded automatically behind our backs

        # Reconstruct the response line.
        if self.__protocol and self.__version:
            proto_ver = "%s/%s " % (self.__protocol, self.__version)
        elif self.__protocol:
            proto_ver = self.__protocol + " "
        elif self.__version:
            proto_ver = self.__version + " "
        else:
            proto_ver = ""
        if self.__status and self.__reason:
            status_line = "%s%s %s\r\n" % (proto_ver, self.__status, self.__reason)
        elif self.__status:
            status_line = "%s%s\r\n" % (proto_ver, self.__status)
        elif self.__reason:
            status_line = "%s%s\r\n" % (proto_ver, self.__reason)

        # Reconstruct the headers.
        if not self.__raw_headers:
            if self.__headers:
                self.__reconstruct_raw_headers()
                raw_headers = self.__raw_headers
            else:
                raw_headers = ""

        # Get the data if available.
        if self.__data:
            data = self.__data
        else:
            data = ""

        # Store the reconstructed raw response.
        self.__raw_response = "%s%s%s" % (status_line, raw_headers, data)


    #----------------------------------------------------------------------
    def __parse_raw_headers(self):
        self.__headers = HTTP_Headers(self.__raw_headers)


    #----------------------------------------------------------------------
    def __reconstruct_raw_headers(self):
        self.__raw_headers = str(self.__headers)
