# Import the Evernote client
from evernote.api.client import EvernoteClient

# For date/time handeling 
from datetime import datetime

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# GUID of the note to retrive the previous version ids of
note_guid = "insert note GUID to retirve versions here"

# Returns a list of previous version for the note inclding title, dates updated and USN
# Use the USN in conjuntion with getNoteVersion to retrive a pervious version of the note
# this method is only avalible to call on account that have Evernote Premium (premium-only feature)
previous_note_ids = note_store.listNoteVersions(note_guid)


print "There are %s previous note versions with USNs of:" % len(previous_note_ids)
for note_id in previous_note_ids:
	print "   * %s updated on %s" % (note_id.updateSequenceNum, datetime.fromtimestamp(note_id.updated/1000))