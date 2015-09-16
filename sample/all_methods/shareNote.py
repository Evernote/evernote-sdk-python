# Import the Evernote client
from evernote.api.client import EvernoteClient

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# The GUID of the note to be shared
note_guid = "insert GUID of note to be shared here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Returns a share key to join to the note via the API to other users
# (see authenticateToSharedNote)
# and/or to create a public link to the note
share_note_key = note_store.shareNote(note_guid)

# Create a public web link to the note 
# https://dev.evernote.com/doc/articles/note_links.php

#Get the User Store
user_store = client.get_user_store()
# Get the webApiUrlPrefix
user_urls = user_store.getUserUrls()
web_prefix = user_urls.webApiUrlPrefix

public_link = web_prefix + "/sh/" + note_guid + "/" + share_note_key

print "You have sucsessfully shared a note from Evernote!"
print "The public link for the note is:\n\n    %s\n" % public_link