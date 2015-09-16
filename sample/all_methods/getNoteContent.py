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

# GUID of the note to retrive the contents of
note_guid = "insert note GUID to retrive the contents here"

# Returns ENML contents of the note with the provided GUID
# For more informaiton on ENML see https://dev.evernote.com/doc/articles/enml.php
enml_note_contents = note_store.getNoteContent(note_guid)


print "ENML of note with GUID '%s': \n\n%s\n\n" % (note_guid, enml_note_contents)

