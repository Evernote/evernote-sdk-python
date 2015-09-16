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

# GUID of the tag to be retrived
tag_guid = 'enter the GUID of the tag to be retrived here'

# Returns the current state of the Tag with the provided GUID.
tag = note_store.getTag(tag_guid)

print "Retrived tag with the name '%s' and GUID '%s'." % (tag.name, tag.guid)