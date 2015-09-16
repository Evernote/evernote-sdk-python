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

# GUID of the note to attach the application data to
note_guid = "insert note GUID to unattach key-value storage to here"

# Key of the application data entry to retrive
key = "your-consumer-key"

#Returns the usn (update service number) of the update
usn = note_store.unsetNoteApplicationDataEntry(note_guid, key)

print "Application data entry for note GUID %s and key '%s' has been unset (USN %s)." % (note_guid, key, usn)

