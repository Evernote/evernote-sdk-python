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

# Note GUID of the note that has the resource to retrive"
note_guid = "insert note GUID with attached resource to retrive here"

# The hex ended string of the MD5 Hash of the binary content that you wish to retrive
# This value is usally present in the ENML where the resource appears in the
# note in the element "en-media" under the attribute "hash"
content_hash = "Insert the hex encoded MD5 hash of the binary fine contents you wish to retrive here"

# Set various Boolean values defining what data and metadata to retrive:
# If true, the Resource will include the binary contents of the 'data' field's body.
with_data = False
# If true, the Resource will include the binary contents of the 'recognition' field's body if recognition data is present.
with_recognition = False
# If true, the Resource will include the binary contents of the 'alternateData' field's body, if an alternate form is present.
with_alternate_data = False

# Returns a string containing the alternate data
# if "EDAMNotFoundException Resource.alternateData" is throw the resource has no recognition
resource = note_store.getResourceByHash(note_guid, content_hash, with_data, with_recognition, with_alternate_data)


print "This resource with the GUID '%s' has the MIME type '%s'." % (resource.guid, resource.mime)

