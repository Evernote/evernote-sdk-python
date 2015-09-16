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

# GUID of the resource to attach the application data to
resource_guid = "insert resource GUID to attach key-value storage to here"

# Value of the key for the storage
# 3rd party apps are only allowed 1
key = "your-consumer-key"

# the value of the application data entry
# containg a string arbitray length 
value = "this is the value of the application data"

# Each note is given this 4kb map of arbitrary data, shared by all third-party applications.
# adding new data may cause the field's value to exceed the the 4kb limit. 
# In this case, an instance of EDAMUserException is thrown with the BAD_DATA_FORMAT error code. 
# Setting this value will overwrite any existing data
usn = note_store.setResourceApplicationDataEntry(resource_guid, key, value)


print "Application data set for resource with GUID, '%s' with the key '%s' and value '%s' (USN %s)" % (resource_guid, key, value, usn)

