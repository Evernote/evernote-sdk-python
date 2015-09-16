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

# insert resource GUID to resource to retrive the alternate data of here"
resource_guid = "insert resource GUID here" 

# Returns a string containing the alternate data
# if "EDAMNotFoundException Resource.alternateData" is throw the resource has no recognition
resource_attributes = note_store.getResourceAttributes(resource_guid)


print "This resource has the file name '%s', and a recognition data type of '%s'." % (resource_attributes.fileName, resource_attributes.recoType)

