# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import the Evernote note storetypes to get note datatypes 
# to properly get note/tag counts (note filter)
import evernote.edam.notestore.ttypes as NoteStoreTypes

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# GUID of the note to retrive
note_guid = "insert note GUID to retrive here"

# Create a result spec object to define what data and
# metadata is to be retuned by the call to getNoteWithResultSpec
result_spec = NoteStoreTypes.NoteResultSpec()
# retrive the content of the note
result_spec.includeContent = False 
# retrive the binary data of the resources attached to this note
result_spec.includeResourcesData = False 
# Include OCR data associated with the resources (if present)
result_spec.includeResourcesRecognition = False
# Include recouce alternate data 
result_spec.includeResourcesAlternateData = False
# Include data on how this note has been shared
result_spec.includeSharedNotes = False


# Returns a list of previous version for the note inclding title, dates updated and USN
# Use the USN in conjuntion with getNoteVersion to retrive a pervious version of the note
# this method is only avalible to call on account that have Evernote Premium (premium-only feature)
note = note_store.getNoteWithResultSpec(note_guid, result_spec)


print "Retrived note with title of '%s'." % note.title