from evernote.client.EvernoteClient import EvernoteClient

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import redirect

EN_CONSUMER_KEY = 'your consumer key'
EN_CONSUMER_SECRET = 'your consumer secret'


def getEvernoteClient(token=None):
    if token:
        return EvernoteClient(token=token, sandbox=True)
    else:
        return EvernoteClient(
            consumerKey=EN_CONSUMER_KEY,
            consumerSecret=EN_CONSUMER_SECRET,
            sandbox=True
        )


def index(request):
    return render_to_response('oauth/index.html')


def auth(request):
    client = getEvernoteClient()
    callbackUrl = 'http://%s%s' % (
        request.get_host(), reverse('evernote_callback'))
    requestToken = client.getRequestToken(callbackUrl)

    # Save the request token information for later
    request.session['oauth_token'] = requestToken['oauth_token']
    request.session['oauth_token_secret'] = requestToken['oauth_token_secret']

    # Redirect the user to the Evernote authorization URL
    return redirect(client.getAuthorizeUrl(requestToken))


def callback(request):
    try:
        client = getEvernoteClient()
        client.getAccessToken(
            request.session['oauth_token'],
            request.session['oauth_token_secret'],
            request.GET.get('oauth_verifier', '')
        )
    except KeyError:
        return redirect('/')

    noteStore = client.getNoteStore()
    notebooks = noteStore.listNotebooks()

    return render_to_response('oauth/callback.html', {'notebooks': notebooks})


def reset(request):
    return redirect('/')
