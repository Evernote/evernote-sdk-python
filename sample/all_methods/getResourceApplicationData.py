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

# GUID of the note to attach the application data to
resource_guid = "insert resource GUID to attach key-value storage to here"

#Returns a lazy map of all the application data associated with the note
application_data = note_store.getResourceApplicationData(resource_guid)

print "Note has %s application data entries:" % len(application_data.fullMap)
for key, value in application_data.fullMap.iteritems():	
	print "   * %s: '%s'" % (key, value)

