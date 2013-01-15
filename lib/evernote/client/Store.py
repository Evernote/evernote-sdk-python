import sys
import functools
import inspect
import re

import evernote.edam.userstore.constants as UserStoreConstants

import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient


class Store(object):

    def __init__(self, token, clientClass, storeUrl):
        self.token = token
        m = re.search(':A=(.+):', token)
        if m:
            self.__userAgentId = m.groups()[0]
        else:
            self.__userAgentId = ''
        self.__client = self.__getThriftClient(clientClass, storeUrl)

    def __getattr__(self, name):
        def delegateMethod(*args, **kwargs):
            targetMethod = getattr(self.__client, name, None)
            if targetMethod is None:
                return object.__getattribute__(self, name)(*args, **kwargs)

            orgArgs = inspect.getargspec(targetMethod).args
            if len(orgArgs) == len(args):
                return targetMethod(*args, **kwargs)
            elif 'authenticationToken' in orgArgs:
                skipArgs = ['self', 'authenticationToken']
                argNames = [item for item in orgArgs if item not in skipArgs]
                return functools.partial(
                    targetMethod, authenticationToken=self.token
                )(**dict(zip(argNames, args)))
            else:
                return targetMethod(*args, **kwargs)

        return delegateMethod

    def __getThriftClient(self, clientClass, url):
        httpClient = THttpClient.THttpClient(url)
        httpClient.addHeaders(**{
            'User-Agent': "%s / %s; Python / %s;"
            % (self.__userAgentId, self.__getSdkVersion(), sys.version)
        })

        thriftProtocol = TBinaryProtocol.TBinaryProtocol(httpClient)
        return clientClass(thriftProtocol)

    def __getSdkVersion(self):
        return '%s.%s' % (
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR
        )
