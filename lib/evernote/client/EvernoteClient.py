import oauth2 as oauth
import urllib
import urlparse

from evernote.client.Store import Store

import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.notestore.NoteStore as NoteStore


class EvernoteClient(object):

    def __init__(self, **options):
        self.consumerKey = options.get('consumerKey')
        self.consumerSecret = options.get('consumerSecret')
        self.sandbox = options.get('sandbox', True)
        if self.sandbox:
            defaultServiceHost = 'sandbox.evernote.com'
        else:
            defaultServiceHost = 'www.evernote.com'
        self.serviceHost = options.get('serviceHost', defaultServiceHost)
        self.additionalHeaders = options.get('additionalHeaders', {})
        self.token = options.get('token')
        self.secret = options.get('secret')

    def getRequestToken(self, callbackUrl):
        client = self.__getOAuthClient()
        requestUrl = '%s?oauth_callback=%s' % (
            self.__getEndpoint('oauth'), urllib.quote(callbackUrl))

        resp, content = client.request(requestUrl, 'GET')
        requestToken = dict(urlparse.parse_qsl(content))
        return requestToken

    def getAuthorizeUrl(self, requestToken):
        return '%s?oauth_token=%s' % (
            self.__getEndpoint('OAuth.action'),
            urllib.quote(requestToken['oauth_token']))

    def getAccessToken(self, oauthToken, oauthTokenSecret, oauthVerifier):
        token = oauth.Token(oauthToken, oauthTokenSecret)
        token.set_verifier(oauthVerifier)
        client = self.__getOAuthClient(token)

        resp, content = client.request(self.__getEndpoint('oauth'), 'POST')
        accessToken = dict(urlparse.parse_qsl(content))
        self.token = accessToken['oauth_token']
        return self.token

    def getUserStore(self):
        userStoreUri = self.__getEndpoint("/edam/user")
        return Store(self.token, UserStore.Client, userStoreUri)

    def getNoteStore(self):
        userStore = self.getUserStore()
        noteStoreUri = userStore.getNoteStoreUrl()
        return Store(self.token, NoteStore.Client, noteStoreUri)

    def getSharedNoteStore(self, linkedNotebook):
        noteStoreUri = linkedNotebook.noteStoreUrl
        noteStore = Store(self.token, NoteStore.Client, noteStoreUri)
        sharedAuth = noteStore.authenticateToSharedNotebook(
            linkedNotebook.shareKey)
        sharedToken = sharedAuth.authenticationToken
        return Store(sharedToken, NoteStore.Client, noteStoreUri)

    def getBusinessNoteStore(self):
        userStore = self.getUserStore()
        bizAuth = userStore.authenticateToBusiness()
        bizToken = bizAuth.authenticationToken
        noteStoreUri = bizAuth.noteStoreUrl
        return Store(bizToken, NoteStore.Client, noteStoreUri)

    def __getOAuthClient(self, token=None):
        consumer = oauth.Consumer(self.consumerKey, self.consumerSecret)
        if token:
            client = oauth.Client(consumer, token)
        else:
            client = oauth.Client(consumer)
        return client

    def __getEndpoint(self, path=None):
        url = "https://%s" % (self.serviceHost)
        if path is not None:
            url += "/%s" % path
        return url
