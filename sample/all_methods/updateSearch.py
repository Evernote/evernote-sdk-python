# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import Evernote types to get service level enum (Basic, Plus, Permium)
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Insert saved search GUID to updated
saved_search_guid = "edbe98cf-3cb6-4ad4-9102-ee438a0660be"#"insert saved search GUID here"

# Get saved search object
# see getSearch for more info
saved_search = note_store.getSearch(saved_search_guid)

# Updated Saved search object
saved_search.name = "Important and recently Created Notes"
saved_search.query = 'any: tag:important created:day-6'
saved_search.scope = Types.SavedSearchScope(includeAccount = True, includePersonalLinkedNotebooks = True, includeBusinessLinkedNotebooks = True)

# Submits search changes to the service. The provided data must include the search's guid field for identification. 
# The service will apply updates to the following search fields: name, query, and scope.
usn = note_store.updateSearch(saved_search)

print "The saved search named '%s' has been updaed (USN %s)." % (saved_search.name, usn)
