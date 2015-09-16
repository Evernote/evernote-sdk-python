# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import the Evernote types to get note datatypes to properly
# create a notebook
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Create the Notebook object
notebook = Types.Notebook()
# Set the name of the notebook
notebook.name = "This is a test notebook"

# Returns a the notebook object as created by the Evernote service
# properties such as "guid", etc. will be filled in by the service.
notebook = note_store.createNotebook( notebook )