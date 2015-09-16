# Import the Evernote client
from evernote.api.client import EvernoteClient

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get user store object
user_store = client.get_user_store()

# Get the user's URLs
user_urls = user_store.revokeLongSession(access_token)

print "The access token\n\n     %s\n\nhas been revoked\n" % access_token
print "You can no longer call the Evernote API with the above access token"