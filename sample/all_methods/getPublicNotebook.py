# Import the Evernote client
from evernote.api.client import EvernoteClient

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# user_id is the numeric identifier for the user who owns the public notebook. 
# To find this value based on a username string, see 'getPublicUserInfo'
user_id = 588345
# The uri string for the public notebook, from Notebook.publishing.uri.
public_uri = "giphy"
# If a notebook is visible on the web with a full URL like http://www.evernote.com/pub/sethdemo/api 
# Then 'sethdemo' is the username that can be used to look up the user_id, and 'api' is the public_uri.

notebook = note_store.getPublicNotebook(user_id, public_uri)


print "Retrived public notebook with title of '%s'." % notebook.name