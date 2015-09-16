# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import the Evernote types to get note datatypes to properly
# create a tag
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Create the tag object
tag = Types.Tag()
# Set the name of the tag
tag.name = "This is a test tag"

# Uncomment the next line to set the (optional) parent tag GUID
#tag.parentGuid = "insert parent tag GUID here"

# Returns a the tag object as created by the Evernote service
# properties such as "guid", etc. will be filled in by the service.
tag = note_store.createTag( tag )