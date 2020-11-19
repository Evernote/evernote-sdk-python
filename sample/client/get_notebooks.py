from evernote2.api.client import EvernoteClient

from configs import evernote_options

# Set up the NoteStore client
client = EvernoteClient(**evernote_options)
note_store = client.get_note_store()

# Make API calls
notebooks = note_store.listNotebooks()
for notebook in notebooks:
    print("Notebook: %s" % notebook.name)
