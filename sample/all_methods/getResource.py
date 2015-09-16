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

# insert resource GUID to resource to retrive here"
resource_guid = "insert resouce GUID here"

# Set various Boolean values defining what data and metadata to retrive:
# If true, the Resource will include the binary contents of the 'data' field's body.
with_data = True
# If true, the Resource will include the binary contents of the 'recognition' field's body if recognition data is present.
with_recognition = True
# If true, the Resource will include the attributes
with_attributes = True
# If true, the Resource will include the binary contents of the 'alternateData' field's body, if an alternate form is present.
with_alternateData = True

# Returns ENML contents of the note with the provided GUID
# For more informaiton on ENML see https://dev.evernote.com/doc/articles/enml.php
resource = note_store.getResource(resource_guid, with_data, with_recognition, with_attributes, with_alternateData)


print "Download resource with the file name '%s', MIME type '%s' and size of %s bytes" % (resource.attributes.fileName, resource.mime, resource.data.size)

