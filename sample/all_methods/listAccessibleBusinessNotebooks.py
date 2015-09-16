# Import the Evernote client
from evernote.api.client import EvernoteClient

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get business note store object
business_store = client.get_business_note_store()

# Returns a list of all the notebooks in a business that the user has permission to access, 
# regardless of whether the user has joined them. This includes notebooks that have been shared 
# with the entire business as well as notebooks that have been shared directly with the user.
accessible_business_notebooks = business_store.listAccessibleBusinessNotebooks()

print "Found %s accessible business notebooks:" % len(accessible_business_notebooks)
for notebook in accessible_business_notebooks:
	print "   * '%s'" % notebook.name