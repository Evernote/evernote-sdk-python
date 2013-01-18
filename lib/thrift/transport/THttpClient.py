#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

from TTransport import TTransportBase
from cStringIO import StringIO

import urlparse
import httplib
import warnings
import socket


class THttpClient(TTransportBase):

    """Http implementation of TTransport base."""

    def __init__(
        self,
        uri_or_host,
        port=None,
        path=None,
        proxy_host=None,
        proxy_port=None
    ):
        """THttpClient supports two different types constructor parameters.

        THttpClient(host, port, path) - deprecated
        THttpClient(uri)

        Only the second supports https."""

        """THttpClient supports proxy
        THttpClient(host, port, path, proxy_host, proxy_port) - deprecated
        ThttpClient(uri, None, None, proxy_host, proxy_port)"""

        if port is not None:
            warnings.warn(
                "Please use the THttpClient('http://host:port/path') syntax",
                DeprecationWarning,
                stacklevel=2)
            self.host = uri_or_host
            self.port = port
            assert path
            self.path = path
            self.scheme = 'http'
        else:
            parsed = urlparse.urlparse(uri_or_host)
            self.scheme = parsed.scheme
            assert self.scheme in ('http', 'https')
            if self.scheme == 'http':
                self.port = parsed.port or httplib.HTTP_PORT
            elif self.scheme == 'https':
                self.port = parsed.port or httplib.HTTPS_PORT
            self.host = parsed.hostname
            self.path = parsed.path
            if parsed.query:
                self.path += '?%s' % parsed.query

        if proxy_host is not None and proxy_port is not None:
            self.endpoint_host = proxy_host
            self.endpoint_port = proxy_port
            self.path = urlparse.urlunparse((
                self.scheme,
                "%s:%i" % (self.host, self.port),
                self.path,
                None,
                None,
                None
            ))
        else:
            self.endpoint_host = self.host
            self.endpoint_port = self.port

        self.__wbuf = StringIO()
        self.__http = None
        self.__timeout = None
        self.__headers = {}

    def open(self):
        protocol = httplib.HTTP if self.scheme == 'http' else httplib.HTTPS
        self.__http = protocol(self.endpoint_host, self.endpoint_port)

    def close(self):
        self.__http.close()
        self.__http = None

    def isOpen(self):
        return self.__http is not None

    def setTimeout(self, ms):
        if not hasattr(socket, 'getdefaulttimeout'):
            raise NotImplementedError

        if ms is None:
            self.__timeout = None
        else:
            self.__timeout = ms / 1000.0

    def read(self, sz):
        return self.__http.file.read(sz)

    def write(self, buf):
        self.__wbuf.write(buf)

    def __withTimeout(f):
        def _f(*args, **kwargs):
            orig_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(args[0].__timeout)
            result = f(*args, **kwargs)
            socket.setdefaulttimeout(orig_timeout)
            return result
        return _f

    def addHeaders(self, **kwargs):
        self.__headers.update(kwargs)

    def flush(self):
        if self.isOpen():
            self.close()
        self.open()

        # Pull data out of buffer
        data = self.__wbuf.getvalue()
        self.__wbuf = StringIO()

        # HTTP request
        self.__http.putrequest('POST', self.path)

        # Write headers
        self.__http.putheader('Host', self.host)
        self.__http.putheader('Content-Type', 'application/x-thrift')
        self.__http.putheader('Content-Length', str(len(data)))
        for key, value in self.__headers.iteritems():
            self.__http.putheader(key, value)
        self.__http.endheaders()

        # Write payload
        self.__http.send(data)

        # Get reply to flush the request
        self.code, self.message, self.headers = self.__http.getreply()

    # Decorate if we know how to timeout
    if hasattr(socket, 'getdefaulttimeout'):
        flush = __withTimeout(flush)
