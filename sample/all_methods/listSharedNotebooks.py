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

# Returns a list of linked notebooks 
shared_notebooks = note_store.listSharedNotebooks()

print "Found %s shared notebooks:" % len(shared_notebooks)
for notebook in shared_notebooks:
	print "   * %s" % notebook.globalId