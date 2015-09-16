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

# Returns the current state of the search with the provided GUID.
saved_searches = note_store.listSearches()

print "Found %s saved searches:" % len(saved_searches)
for search in saved_searches:
	print "   '%s'" % search.query