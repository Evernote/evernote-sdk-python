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
resource_guid = "insert the GUID of the resource you would like to retrive the data of here"

# Returns a string with the binary data of the resource
resource_data = note_store.getResourceData(resource_guid)

# Write the data to a file
with open(resource_guid, 'w') as f:
	f.write(resource_data)
	f.close()

print "Resource data has been downloaded"

