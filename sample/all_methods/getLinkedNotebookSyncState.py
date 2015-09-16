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

# Get a list of linked notebooks 
# for more info see listLinkedNotebooks
linked_notebooks = note_store.listLinkedNotebooks()

# Filter to just get notebooks that are not a part of the user's business
# if you need to sync business content authenticate to business first and then
# call getSyncState and getFilteredSyncChunk on the business note store
# Get business ID
business_id = client.get_user_store().getUser().accounting.businessId
# Filter out all business notebooks that are from the user's business
if business_id:
	linked_notebooks = [ lknb for lknb in linked_notebooks if lknb.businessId != business_id  ]


# Get a indivudual linked notebook
linked_notebook = linked_notebooks[0]

# Returns a sync state object that contains information on the sync state of the linked notebook
# including the USN, the monotomically increseaing integer to indicate when updates have
# occured as indicated by the Evernote service
sync_state = note_store.getLinkedNotebookSyncState(linked_notebook)

print "The USN at %s for the linked notebook '%s' is %s." %  ( datetime.fromtimestamp(sync_state.currentTime/1000), linked_notebook.shareName, sync_state.updateCount )