# Import the Evernote client
from evernote.api.client import EvernoteClient

# For date/time handeling 
from datetime import datetime

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Returns a sync state object that contains information on the sync state of the account
# including the USN, the monotomically increseaing integer to indicate when updates have
# occured as indicated by the Evernote service
sync_state = note_store.getSyncState()

print "The USN at %s is %s." %  ( datetime.fromtimestamp(sync_state.currentTime/1000), sync_state.updateCount )