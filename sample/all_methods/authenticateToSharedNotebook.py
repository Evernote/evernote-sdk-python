# Import the Evernote client and generic Store type
from evernote.api.client import EvernoteClient, Store

# Import the NoteStore type to create a note store object
# that connects to the note store which contains the note
# that has been shared to the user
import evernote.edam.notestore.NoteStore as NoteStore

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# The global ID of the notebook as indicated by the linked notebook object attribute "sharedNotebookGlobalId"
notebook_global_id = "insert the global ID of the notebook to authenticate to"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Returns a share key to join to the note via the API to other users
# (see authenticateToSharedNote)
# and/or to create a public link to the note
auth_result = note_store.authenticateToSharedNotebook( notebook_global_id, access_token )

if auth_result.authenticationToken:
	#create a new note store object corresponding to the note store that contians the shared note
	shared_note_store = Store(token = auth_result.authenticationToken, client_class =NoteStore.Client, store_url = auth_result.noteStoreUrl)
	
	#Get the shared note (see getNote for more information)
	shared_notebook = shared_note_store.getNotebook(note_guid, True, True, True, True)

	print "The notebook shared to this user has the name '%s'" % shared_notebook.name

else:
	print "authentication failed"