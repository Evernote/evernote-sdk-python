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

# Returns a list of linked notebooks 
all_linked_notebooks = note_store.listLinkedNotebooks()

# Filter to just get notebooks that are not a part of the user's business
# if you need to sync business content authenticate to business first and then
# call getSyncState and getFilteredSyncChunk on the business note store
# Get business ID
business_id = client.get_user_store().getUser().accounting.businessId
# Filter out all business notebooks that are from the user's business
if business_id:
	linked_notebooks = [ lknb for lknb in all_linked_notebooks if lknb.businessId != business_id  ]

print "Found %s linked notebooks:" % len(linked_notebooks)
for notebook in linked_notebooks:
	print "   * '%s'" % notebook.shareName