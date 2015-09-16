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

# GUID of the note to retrive the search contents of
note_guid = "insert GUID here"

# If true, will only return text from the note contents
# If false will return text from the note and any attachment 
# recofnition sources (i.e. text from PDFs, OCRed images)
note_only = False

# If true, this will break the text into cleanly separated and sanitized tokens. 
# If false, this will return the more raw text extraction, with its original punctuation, capitalization, spacing, etc.
tokenized = False

# Returns plain text contents of the note with the provided GUID
note_search_text = note_store.getNoteSearchText(note_guid, note_only, tokenized)


print "Note search text of note with GUID '%s': \n\n%s\n\n" % (note_guid, note_search_text)