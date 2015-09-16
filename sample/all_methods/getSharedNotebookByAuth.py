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

# Get a shared notebook access token from authenticateToSharedNotebook 
shared_notebook_access_token = 'Insert shared notebook authenitcaiton token here'

# This function is used to retrieve extended information about a shared notebook by a guest who has already authenticated 
# to access that notebook. This requires an 'authenticationToken' parameter which should be the resut of a call to 
# authenticateToSharedNotebook(...). I.e. this is the token that gives access to the particular shared notebook in someone else's 
# account -- it's not the authenticationToken for the owner of the notebook itself.
shared_notebook = note_store.getSharedNotebookByAuth(shared_notebook_access_token)

print "The shared notebook object for the notebook with GUID '%s' has been retrived." % shared_notebook.notebookGuid