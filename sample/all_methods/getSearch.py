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

# insert saved search GUID
# to get a list of saved searches and their GUIDs
# see listSearches or createSearch
saved_search_guid = "insert saved search GUID here"

# Returns the current state of the search with the provided GUID.
saved_search = note_store.getSearch(saved_search_guid)

print "Retrived saved search named '%s' with query '%s'" % (saved_search.name, saved_search.query)

