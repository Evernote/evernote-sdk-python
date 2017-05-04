# http://blog.evernote.com/blog/2011/10/21/did-you-know-note-links-and-how-to-use-them/
from evernote.api.client import EvernoteClient, NoteStore

# https://sandbox.evernote.com/api/DeveloperToken.action
dev_token = "<enter your own developer token>"

class EvernoteSession:
    
    def __init__(self, dev_token):
        self.token = dev_token
        self.client = EvernoteClient(token=dev_token)
        self.userStore = self.client.get_user_store()
        self.noteStore = self.client.get_note_store()
        
    def internalNoteLink(self, noteGuid):
        # Original: evernote:///view/13708770/s129/abe5f3b4-b305-4172-b5c9-985cc2ba5e78//
        # Stripped: evernote:///view/0/s129/abe5f3b4-b305-4172-b5c9-985cc2ba5e78/00000000-0000-0000-0000-000000000000/
        # Template: evernote:///view/<ownerid>/<shardid>/<noteguid>/<localvalue>/<linkedNotebookValue>
        user = self.userStore.getUser()
        shardId = user.shardId   
        userId = user.id
        localWTF = "00000000-0000-0000-0000-000000000000"
        return "%sview/%d/%s/%s/%s/" % ("evernote:///", userId, shardId, noteGuid, localWTF)

    def listAllNotes(self):
        noteFilter = NoteStore.NoteFilter()
        # http://dev.evernote.com/documentation/reference/NoteStore.html#Struct_NoteFilter
        # notebook = self.noteStore.getDefaultNotebook()
        # noteFilter.notebookGuid = notebook.guid
        searchResults = self.noteStore.findNotes(self.token, noteFilter, 0, 50)
        return searchResults.notes
        
if __name__=="__main__":
    c = EvernoteSession(dev_token)
    print "Connected as '%s'" % (c.userStore.getUser().username)
    print
    notes = c.listAllNotes()
    for note in notes:
        print "%-40s => %s" % (note.title, c.internalNoteLink(note.guid))
    