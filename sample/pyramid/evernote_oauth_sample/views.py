from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from evernote.api.client import EvernoteClient


def _get_evernote_client(request):
    session = request.session
    access_token = session.get('access_token')

    if access_token:
        return EvernoteClient(
            token=access_token,
            sandbox=True)
    else:
        settings = request.registry.settings
        consumer_key = settings.get('evernote.consumer_key')
        consumer_secret = settings.get('evernote.consumer_secret')

        return EvernoteClient(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            sandbox=True)


@view_config(route_name='home', renderer='home.mak')
def home(request):
    return {}


@view_config(route_name='evernote_auth')
def evernote_oauth(request):
    session = request.session
    session.invalidate()

    client = _get_evernote_client(request)
    request_token = client.get_request_token(
        request.route_url('evernote_callback'))
    session['oauth_token'] = request_token['oauth_token']
    session['oauth_token_secret'] = request_token['oauth_token_secret']

    authorized_url = client.get_authorize_url(request_token)

    return HTTPFound(authorized_url)


@view_config(route_name='evernote_callback', renderer='callback.mak')
def evernote_callback(request):
    client = _get_evernote_client(request)
    session = request.session

    oauth_verifier = request.params.get('oauth_verifier')
    oauth_token = session.get('oauth_token')
    oauth_token_secret = session.get('oauth_token_secret')

    if oauth_verifier and oauth_token and oauth_token_secret:
        access_token = client.get_access_token(
            oauth_token,
            oauth_token_secret,
            oauth_verifier)

        session['access_token'] = access_token

        return HTTPFound('notebooks')

    return HTTPBadRequest(
        'oauth_verifier, oauth_token or oauth_token_secret not found')


@view_config(route_name='notebooks', renderer='notebooks.mak')
def notebooks(request):
    client = _get_evernote_client(request)
    note_store = client.get_note_store()
    return {'notebooks': note_store.listNotebooks()}


@view_config(route_name='evernote_auth_reset')
def evernote_oauth_rest(request):
    request.session.invalidate()
    return HTTPFound(request.route_url('home'))
