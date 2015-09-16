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

# Define the notebook GUID you wish to get the tags of
notebook_guid = "Insert notebook GUID here"

# Returns a list of linked notebooks 
tags = note_store.listTagsByNotebook(notebook_guid)

print "Found %s tags attached to notes in the notebook with the GUID %s" % (len(tags), notebook_guid)
for tag in tags:
	print "   * %s" % tag.name