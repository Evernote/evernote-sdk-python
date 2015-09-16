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

# insert resource GUID
resource_guid = "insert resource GUID here"

# Returns a block of the extracted plain text contents of the resource with the provided GUID.
resource_search_text = note_store.getResourceSearchText(resource_guid)

print "Resource search text data for the resource with GUID %s: \n\n%s\n\n" % (resource_guid, resource_search_text)

