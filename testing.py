import unittest
from evernote.api.client import EvernoteClient as ec
from evernote.edam.type.ttypes import Notebook, Note
from evernote.edam.notestore.ttypes import SyncChunkFilter

"""
Test cases:
	* every API CALL?!?!
"""

class TestEvernote(unittest.TestCase):
	def setUp(self):
		self.c=ec(token="nope", sandbox=False)
		self.us=self.c.get_user_store()
		self.ns=self.c.get_note_store()

	def test_ns_list_notebooks(self):
		# get list of notebooks
		notebooks_list=self.ns.listNotebooks()
		
		# test that more than 0 notebooks are returned
		self.assertGreater(len(notebooks_list), 0)

		#test that each item in the list is a notebook
		for notebook in notebooks_list:
			self.assertEqual(type(notebook), type(Notebook()))

	def test_us_get_user_urls(self):
		#get store urls
		userStoreUrl=self.us.getUserUrls().userStoreUrl[:4]
		noteStoreUrl=self.us.getUserUrls().noteStoreUrl[:4]
		
		#test that urls are valid addresses
		self.assertEqual(userStoreUrl, "http")
		self.assertEqual(noteStoreUrl, "http")

	def test_ns_get_default_notebook(self):
		#get default notebook
		defaultNotebook = self.ns.getDefaultNotebook()

		#test that the default notebook is a notebook
		self.assertEqual(type(defaultNotebook), type(Notebook()))

	def test_ns_note_create_copy_update_delete(self):
		#test note creation
		note=Note()
		note.title = "Automated Test Note"
		note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\"><en-note>Hello World!!</en-note>"
		note=self.ns.createNote(note)
		self.assertEqual(type(note), type(Note()))

		# test note copying
		defaultNotebook = self.ns.getDefaultNotebook()
		copiedNote = self.ns.copyNote(note.guid, defaultNotebook.guid)

		#test updating a note
		copiedNote.content="<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\"><en-note>Evernote</en-note>"
		self.ns.updateNote(copiedNote)

		# test note deletion
		self.ns.deleteNote(note.guid)
		self.ns.deleteNote(copiedNote.guid)

	def test_ns_notebook_create_get_update(self):
		#create notebook
		notebook = Notebook()
		notebook.name = "Test"
		notebook = self.ns.createNotebook(notebook)

		#get notebook
		notebook_get = self.ns.getNotebook(notebook.guid)
		self.assertEqual(notebook_get, notebook)

		#update notebook
		new_notebook_title = "Test Altered Title"
		notebook.name = new_notebook_title
		self.ns.updateNotebook(notebook)
		
		#test name integrity
		self.assertEqual(notebook.name, new_notebook_title)

		#cleanup (delete test notebook)
		self.ns.expungeNotebook(notebook.guid)

	def test_ns_syncstate_syncchunk(self):
		#get sync state
		self.ns.getSyncState()
		
		#get filtered sync chunk
		scf = SyncChunkFilter()
		sc = self.ns.getFilteredSyncChunk(0, 5, scf)






		







if __name__ == "__main__":
	unittest.main()