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

# The GUID of the note to be un-shared.
note_to_unshare_guid = "Insert GUID of note to unshare here"

# If this note is shared publicly then this will stop sharing that note and invalidate its "Note Key", 
# so any existing URLs to access that Note will stop working.
# If the Note is not shared, then this function will do nothing.
# Returns nothing
share_note_key = note_store.stopSharingNote(note_to_unshare_guid)

print "You have sucsessfully unshared the note with GUID '%s'." % note_to_unshare_guid