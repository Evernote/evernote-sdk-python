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

# GUID of the note to retrive the tag names of
note_guid = "insert note GUID to get the attached list names here"

# Returns a list of tag name that are attached to the note
attached_tags = note_store.getNoteTagNames(note_guid)


print "Note has %s tag(s) attached:" % len(attached_tags)
for tag in attached_tags:
	print "   * '%s'" % tag