# Import the Evernote client
from evernote.api.client import EvernoteClient

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "S=s1:U=8fa39:E=1570c5cbbc0:C=14fb4ab8dd0:P=1cd:A=internal-dev:V=2:H=89aad37d3ee09556f6dca063e60bbe48" 

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# GUID of the note to attach the application data to
note_guid = "insert note GUID to unattach key-value storage to here"

# Key of the application data entry to retrive
key = "your-consumer-key"

#Returns the usn (update service number) of the update
usn = note_store.unsetResourceApplicationDataEntry(note_guid, key)

print "Application data entry for resource GUID %s and key '%s' has been unset (USN %s)." % (note_guid, key, usn)

