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

# Get resource object to update
# see getResource for more info
resource = note_store.getResource(resource_guid, True, True, True, True)

# Make the desired changes to the resource object
# Update the file name of the resource
resource.attributes.fileName = "this is an updated filename"
# Forces the display of the resource as an attachment and not to be displayed inline
resource.attributes.attachment = True
# You can also alter the binary file data by updating the data object contained in the
# data attribute of the resource object.   If you do be sure to update the bodyHash and
# size attributes of the data attribute as well as the body in addition to updating the
# hash of the en-media element in the note's contents.

#Returns the usn (update service number) of the update
usn = note_store.updateResource(resource)

print "Updated resource with the file name '%s', MIME type '%s' and size of %s bytes (USN %s)." % (resource.attributes.fileName, resource.mime, resource.data.size, usn)