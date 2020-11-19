from django.conf.urls import include, url
from oauth import views as oauth_views

urlpatterns = [
    url(r"^$", oauth_views.index, name="evernote_index"),
    url(r"^auth/$", oauth_views.auth, name="evernote_auth"),
    url(r"^callback/$", oauth_views.callback, name="evernote_callback"),
    url(r"^reset/$", oauth_views.reset, name="evernote_auth_reset"),
]