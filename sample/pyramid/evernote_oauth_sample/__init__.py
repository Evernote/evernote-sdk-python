from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('evernote_auth', '/auth')
    config.add_route('evernote_callback', '/callback')
    config.add_route('evernote_auth_reset', '/reset')
    config.add_route('notebooks', '/notebooks')
    config.scan()
    return config.make_wsgi_app()
