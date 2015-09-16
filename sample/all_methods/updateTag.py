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
tag_guid = "aeb1e73a-e26b-4133-99a6-b6f7fc532c8d"#'enter the GUID of the tag to be retrived here'
# Get the tag (see getTag for more info)
tag = note_store.getTag(tag_guid)

# Update tag
tag.name = "Newly updated tag name"
#tag.parentGuid = "Insert parent tag GUID here"

# Submits tag changes to the service. 
# The provided data must include the tag's guid field for identification. 
# The service will apply updates to the following tag fields: name, parentGuid
usn = note_store.updateTag(tag)

print "Updated tag with the name '%s' (USN %s)." % (tag.name, usn)