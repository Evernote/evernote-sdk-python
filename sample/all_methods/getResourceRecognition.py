# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import XML library for recognition data formatting
from xml.dom.minidom import parseString

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

# Returns the XML contents of the recognition index for the resource with the provided GUID
# If the caller asks about a resource that has no recognition data, this will throw EDAMNotFoundException
# For more information see https://dev.evernote.com/doc/articles/image_recognition.php
resource_recognition = note_store.getResourceRecognition(resource_guid)

parsed_xml = parseString(resource_recognition)

print "Resource recognition data for the resource with GUID %s: \n\n%s\n\n" % (resource_guid, parsed_xml.toprettyxml())

