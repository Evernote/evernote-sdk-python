# Import the Evernote client and generic Store type
from evernote.api.client import EvernoteClient

# Import the Evernote types to get note datatypes to properly
# create a note
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Create the Note object
note = Types.Note()
# Set the title of the note
note.title = "This is a test note"
# Set the content of the note for more infomormation on ENML, see https://dev.evernote.com/doc/articles/enml.php
note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
note.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
note.content += "<en-note>This note was created using Evernote's Python SDK!</en-note>"
# uncomment the next line to set (optional) notebook GUID (if not set it will be put in the user's default notebook)
#note.notebookGuid = " insert notebook GUID here"
# uncomment the next line to set (optional) tag GUIDs.  See createTag for more information
#note.tagGuids = ["insert tag GUID #1",  "insert tag GUID #2", "insert tag GUID #3", "..."] 
#  uncomment the next line to attach (optional) resources to a note.  See updateResource for more information.
#note.resources = ["insert Resource Object #1",  "insert Resource Object #2", "insert Resource Object #3", "..."] 

# Returns a the note object as created by the Evernote service
# properties such as "guid", "contentHash", "contentLength", etc. will
# be filled in by the service.
note = note_store.createNote( note )