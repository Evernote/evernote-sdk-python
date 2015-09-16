# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import the Evernote types to get note datatypes to properly
# create a Search
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Create the Saved Search object
saved_search = Types.SavedSearch()
# Set the name of the saved search
saved_search.name = "This is a test saved search"

# Set the saved search query.  See Search Grammer for more info
saved_search.query = "any: -intitle:coffee -notebook:Private -tag:hate resource:* todo:false created:day-2"

# Create a SearchScope object
scope = Types.SavedSearchScope()
# Set the scope for personal, shared and business notebooks
scope.includeAccount = True
scope.includePersonalLinkedNotebooks = True
scope.includeBusinessLinkedNotebooks = True
# Attach the scope object to the SavedSearch object
saved_search.scope = scope

# Returns a the saved search object as created by the Evernote service
# properties such as "guid", etc. will be filled in by the service.
saved_search = note_store.createSearch( saved_search )