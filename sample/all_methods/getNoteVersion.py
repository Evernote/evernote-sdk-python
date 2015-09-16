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

# GUID of the note to retrive the previous versions of
note_guid = "insert note GUID to retrive previous versions of here"

# USN of a previous update to the note from when you would like to retirve the note
# for a list of previous USNs see the method "listNoteVersions"
# this method is only avalible to call on account that have Evernote Premium (premium-only feature)
usn = 1617

# Boolean values to include various portions of resource data and metadata:
include_resources = False
include_resoruce_recognition = False
include_alternate_data = False

# Returns a list of tag name that are attached to the note
versioned_note = note_store.getNoteVersion(note_guid, usn, include_resources, include_resoruce_recognition, include_alternate_data)


print "The pervious version of the note titled '%s' has been retrived.  This version of the note was last updated on %s" % (versioned_note.title, datetime.fromtimestamp(versioned_note.updated/1000))