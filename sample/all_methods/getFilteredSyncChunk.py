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

# Set maximum entries for the sync chunck to return
max_entries = 100

# Set the USN of the update you want to get data after
# i.e. if you app has data since USN 1111 enter USN 1111 to get updates
# for content updated/created after USN 1111
after_USN =0

# Create sync chunk filter object
sync_filter = NoteStoreTypes.SyncChunkFilter()
# Set boolean attributes of the sync filter:
sync_filter.includeNotes = True
sync_filter.includeNoteResources = False
sync_filter.includeNoteAttributes = True
sync_filter.includeNotebooks = True
# sync_filter.includeTags = False
# sync_filter.includeSearches = False
# sync_filter.includeResources = False
# sync_filter.includeLinkedNotebooks = True
# #sync_filter.includeExpunged = False
# sync_filter.includeNoteApplicationDataFullMap = True
# sync_filter.includeResourceApplicationDataFullMap = True
# sync_filter.includeNoteResourceApplicationDataFullMap = True
# sync_filter.includedSharedNotes = True
# sync_filter.omitSharedNotebooks = False
#sync_filter.requireNoteContentClass	= 'evernote.contact.1'
#sync_filter.notebookGuids = ["aafdb794-7207-4fa5-8d69-fdb3a87f031d"]#["Notebook GUID 1", "Notebook GUID 2", "Notebook GUID 3", "..."]

# Returns a notebook object that is the user's default notebook
# as created by the Evernote service
sync_chunk = note_store.getFilteredSyncChunk(after_USN, max_entries, sync_filter)


if not sync_chunk.notes and not sync_chunk.notebooks and not sync_chunk.tags:
	print "No sync chunk recived."
else:
	print "Recivied sync chunk:"	

if sync_chunk.notes:
	print "    * %s note(s)" % len(sync_chunk.notes)
if sync_chunk.notebooks:
	print "    * %s notebook(s)" % len(sync_chunk.notebooks)
if sync_chunk.tags:
	print "    * %s tag(s)" % len(sync_chunk.tags)