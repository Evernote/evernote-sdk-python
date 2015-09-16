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

# Get a list of personal notebooks 
notebooks = note_store.listNotebooks()

# Get a notebook object
# If you already have on in your code you can start here
notebook = notebooks[0]

# Make updates to the notebook object
notebook.name = "this is a new name for the notebook"
notebook.stack = "this is a test stack"

#Returns the usn (update service number) of the update
usn = note_store.updateNotebook(notebook)

print "The notebook with the name '%s' has been updated (USN %s)." % (notebook.name, usn)