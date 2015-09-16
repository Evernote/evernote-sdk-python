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

# Get a linked notebook object
# If you already have on in your code you can start here
linked_notebook = linked_notebooks[0]

# Make updates to the linked notebook object
linked_notebook.shareName = "this is a new name for the linked notebook"
linked_notebook.stack = "this is a test stack"

#Returns the usn (update service number) of the update
usn = note_store.updateLinkedNotebook(linked_notebook)

print "The linked notebook with the name '%s' has been updated (USN %s)." % (linked_notebook.shareName, usn)

