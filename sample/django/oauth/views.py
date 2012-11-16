import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.notestore.NoteStore as NoteStore
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
import oauth2 as oauth
import urllib
import urlparse

EN_CONSUMER_KEY = 'your consumer key'
EN_CONSUMER_SECRET = 'your consumer secret'
EN_HOST = "sandbox.evernote.com"

EN_REQUEST_TOKEN_URL = "https://" + EN_HOST + "/oauth"
EN_ACCESS_TOKEN_URL = "https://" + EN_HOST + "/oauth"
EN_AUTHORIZE_URL = "https://" + EN_HOST + "/OAuth.action"

EN_USERSTORE_URIBASE = "https://" + EN_HOST + "/edam/user"


def get_oauth_client(token=None):
    consumer = oauth.Consumer(EN_CONSUMER_KEY, EN_CONSUMER_SECRET)
    if token:
        client = oauth.Client(consumer, token)
    else:
        client = oauth.Client(consumer)
    return client


def getUserStore():
    userStoreHttpClient = THttpClient.THttpClient(EN_USERSTORE_URIBASE)
    userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
    userStore = UserStore.Client(userStoreProtocol)
    return userStore


def getNoteStore(authToken):
    userStore = getUserStore()
    noteStoreUrl = userStore.getNoteStoreUrl(authToken)
    noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
    noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
    noteStore = NoteStore.Client(noteStoreProtocol)
    return noteStore


def index(request):
    return render_to_response('oauth/index.html')


def auth(request):
    client = get_oauth_client()
    callback_url = 'http://%s%s' % (
        request.get_host(), reverse('evernote_callback'))
    request_url = '%s?oauth_callback=%s' % (
        EN_REQUEST_TOKEN_URL, urllib.quote(callback_url))

    resp, content = client.request(request_url, 'GET')
    request_token = dict(urlparse.parse_qsl(content))

    # Save the request token information for later
    request.session['oauth_token'] = request_token['oauth_token']
    request.session['oauth_token_secret'] = request_token['oauth_token_secret']

    # Redirect the user to the Evernote authorization URL
    return redirect('%s?oauth_token=%s' % (
        EN_AUTHORIZE_URL, urllib.quote(request.session['oauth_token'])))


def callback(request):
    oauth_verifier = request.GET.get('oauth_verifier', '')

    try:
        token = oauth.Token(
            request.session['oauth_token'],
            request.session['oauth_token_secret'])
        token.set_verifier(oauth_verifier)

        client = get_oauth_client(token)

        resp, content = client.request(EN_ACCESS_TOKEN_URL, 'POST')

        access_token = dict(urlparse.parse_qsl(content))
        auth_token = access_token['oauth_token']
    except KeyError:
        return redirect('/')

    noteStore = getNoteStore(auth_token)
    notebooks = noteStore.listNotebooks(auth_token)

    return render_to_response('oauth/callback.html', {'notebooks': notebooks})


def reset(request):
    return redirect('/')
