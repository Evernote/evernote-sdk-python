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

# GUID of the notebook to retrive
notebook_guid = "insert GUID of notebook here"

# Returns a notebook corresponding to the supplied GUID
notebook = note_store.getNotebook(notebook_guid)


print "Retrived notebook with title of '%s'." % notebook.name