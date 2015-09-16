# Import the Evernote client and generic Store type
from evernote.api.client import EvernoteClient

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# The GUID of the note to be copied
note_guid_to_copy = "insert the GUID of the note to be copied"

# The GUID of the destination notebook
destination_notebook_guid= "insert the GUID of the notebook that the note will be copied to"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Returns a the copied note object
copied_note = note_store.copyNote( note_guid_to_copy, destination_notebook_guid )