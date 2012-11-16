from django.conf.urls import patterns, url


urlpatterns = patterns(
    'oauth.views',
    url(r"^$", "index", name="evernote_index"),
    url(r"^auth/$", "auth", name="evernote_auth"),
    url(r"^callback/$", "callback", name="evernote_callback"),
    url(r"^reset/$", "reset", name="evernote_auth_reset"),
)
