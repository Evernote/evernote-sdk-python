# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import the Evernote note storetypes to get note datatypes 
# to properly get note/tag counts (note filter)
import evernote.edam.notestore.ttypes as NoteStoreTypes

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Create note filter object
note_filter = NoteStoreTypes.NoteFilter()

# Set note filter search grammer to get notes created in the last 2 days
note_filter.words = "updated:month-2"

# Uncommend the following line to set note filter tag GUIDs
#note_filter.tagGuids = ["GUID of tag1", "GUID of tag 2", "...."]

# Set note filter order to descending
note_filter.ascending =  False

# Set note filter inative attribute to False (will search only active notes)
# setting this value to True will only return search results that are in the trash
note_filter.inactive = False

# Uncomment the following line to set note time zone of the search to 'America/Los_Angeles'
#note_filter.timeZone = "America/Los_Angeles"

# Uncomment the following line to set note filter emphasized attribute to additional 
# 'wish list' search grammer to be used in conjunction with the orinigal search query to 
# highlight search results 
#note_filter.emphasized = "any: tag:cool -tag:uncool"

# Uncomment the following line to set note filter includeAllReadableNotebooks attribute
# to include all readable business notebooks in a search
# search must be performed on a business note store with a business auth token
#note_filter.includeAllReadableNotebooks=True

# Create a result spec object for the findNotesMetadata method
result_spec = NoteStoreTypes.NotesMetadataResultSpec()
# Set various boolean parameters (optional)
result_spec.includeTitle = True
result_spec.includeContentLength = True
result_spec.includeCreated = True
result_spec.includeUpdated = True
result_spec.includeDeleted = True
result_spec.includeUpdateSequenceNum = True
result_spec.includeNotebookGuid = True
result_spec.includeTagGuids = True
result_spec.includeAttributes = True
result_spec.includeLargestResourceMime = True
result_spec.includeLargestResourceSize = True

# Set search result offset (0 for first search)
offset = 0

# Set maximum number of notes to be returned (250 maximum)
max_notes = 250

search_result = note_store.findNotesMetadata( note_filter, offset, max_notes, result_spec)

print "Found %s notes.\n" % search_result.totalNotes
if search_result.totalNotes >= 3:
	print "Here are the titles of 3 of them:\n  * '%s'\n  * '%s'\n  * '%s'" % (search_result.notes[0].title, search_result.notes[1].title, search_result.notes[2].title)
