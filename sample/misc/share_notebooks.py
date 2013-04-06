import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient, NoteStore, UserStore

# https://sandbox.evernote.com/api/DeveloperToken.action
dev_token = "<enter your own developer token>"

class EvernoteSession:
    
    def __init__(self, dev_token):
        self.token = dev_token
        self.client = EvernoteClient(token=dev_token)
        self.userStore = self.client.get_user_store()
        self.noteStore = self.client.get_note_store()
        
    # def listAllNotes(self, notebookGuid=None):
    #     noteFilter = NoteStore.NoteFilter()
    #     # http://dev.evernote.com/documentation/reference/NoteStore.html#Struct_NoteFilter
    #     if notebookGuid:
    #         noteFilter.notebookGuid = notebookGuid
    #     searchResults = self.noteStore.findNotes(self.token, noteFilter, 0, 50)
    #     return searchResults.notes

    def shareNotebook(self, notebookGuid, email=None):
        sharedNotebook = Types.SharedNotebook()
        sharedNotebook.requireLogin = True
        sharedNotebook.notebookGuid = notebookGuid
        sharedNotebook.email = email
        sharedNotebook.privilege = Types.SharedNotebookPrivilegeLevel.READ_NOTEBOOK_PLUS_ACTIVITY

        newSharedNotebook = c.noteStore.createSharedNotebook(c.token, sharedNotebook)

        user = self.userStore.getUser()
        shardId = user.shardId

        url = "%s/shard/%s/share/%s/" % (EN_URL, shardId, newSharedNotebook.shareKey)
        return url
        
if __name__=="__main__":
    c = EvernoteSession(dev_token)
    
    print "Connected as '%s'" % (c.userStore.getUser().username)

    while 1:        
        print
        notebooks = c.noteStore.listNotebooks()
        sharedNotebooks = c.noteStore.listSharedNotebooks()
        
        ctr = 0
        for notebook in notebooks:
            print "Notebook [%d] '%s'" % (ctr, notebook.name)
            ctr += 1
            
            for sharedNotebook in sharedNotebooks:
                if sharedNotebook.notebookGuid == notebook.guid:
                    print "- Shared with %s" % (sharedNotebook.email)
                    # for note in c.listAllNotes(notebook.guid):
                    #     print "-", note.title, note.guid
        
        print
        ch = raw_input("Share notebook number: ")
        print
        
        if not len(ch):
            break
        
        n = int(ch)        
        notebook = notebooks[n]

        email = "dirk@evernote.com"
        url = c.shareNotebook(notebook.guid, email)
        print "Send URL to %s => %s" % (email, url)
        