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
user_urls = user_store.getUserUrls()

print "This user's note store URL is %s" % user_urls.noteStoreUrl
print "This user's user store URL is %s" % user_urls.userStoreUrl



