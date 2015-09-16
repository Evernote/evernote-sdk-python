# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import the Evernote note store types to get note datatypes 
# to properly get a note (note filter)
import evernote.edam.notestore.ttypes as NoteStoreTypes

# For timestamp handeling 
from time import time

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# GUID of note to be updated
note_guid = "insert note GUID to updated here"

# Get the most recent version of the note to prevent note conflicts
# for more information see getNoteWithResultSpec
result_spec = NoteStoreTypes.NoteResultSpec()
result_spec.includeContent = False 
result_spec.includeResourcesData = False 
result_spec.includeResourcesRecognition = False
result_spec.includeResourcesAlternateData = False
result_spec.includeSharedNotes = False
note = note_store.getNoteWithResultSpec(note_guid, result_spec)

# Make the desired changes to the note object
# Check the USN of the note:
print "The current USN of the ntoe is %s" % note.updateSequenceNum
# Update the title of the note
note.title = "the note title is now updated"
# Update the content of the note
note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
note.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
note.content += "<en-note>This note was updated using Evernote's Python SDK!</en-note>"
# Update the update timestamp of the note
# Evernote uses UNIX timestamps in miliseconds
note.updated = int(time()*1000)
# You can also change tags, resources, what notebook the note is in (change the notebookGuid attribute)
# and any other property of the note object

# Submit a set of changes to a note to the service. 
# Perform the same operation as updateNote() would provided that the update sequence number on the 
# parameter Note object matches the current update sequence number that the service has for the note. 
# If they do not match, then no update is performed and the return value will have the current server state
# in the note field and updated will be false. If the update sequence numbers between the client and server 
# do match, then the note will be updated and the note field of the return value will be returned as it 
# would be for the updateNote method. 
print "attempting to update the note..."
update_result = note_store.updateNoteIfUsnMatches(note)

if update_result.updated:
	note = update_result.note
	print "The note with the title '%s' has been updated (USN %s)." % (note.title, note.updateSequenceNum)
else:
	print "Note was not updated, please check to make sure you have an up to date version of the note."

