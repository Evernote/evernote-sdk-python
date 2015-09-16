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

# Removes the provided tag from every note that is currently tagged with this tag. 
# If this operation is successful, the tag will still be in the account, but it will not be tagged on any notes.
note_store.untagAll(tag_guid)

print "Untagged all notes with the tag GUID %s." % tag_guid