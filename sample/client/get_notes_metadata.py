from configs import evernote_options

from evernote2.api.client import EvernoteClient
from evernote2.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote2.edam.type.ttypes import NoteSortOrder


# Set up the NoteStore client
client = EvernoteClient(**evernote_options)
note_store = client.get_note_store()

updated_filter = NoteFilter(order=NoteSortOrder.UPDATED)
offset = 0
max_notes = 10
result_spec = NotesMetadataResultSpec(includeTitle=True)
result_list = note_store.findNotesMetadata(updated_filter, offset, max_notes, result_spec)

# note is an instance of NoteMetadata
# result_list is an instance of NotesMetadataList
print('======= batch 1')
for idx, note in enumerate(result_list.notes):
    print(idx, note.title)

print('======= batch 2')
offset = 10
result_list = note_store.findNotesMetadata(updated_filter, offset, max_notes, result_spec)
for idx, note in enumerate(result_list.notes):
    print(idx, note.title)
