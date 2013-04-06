from evernote.api.client import EvernoteClient, NoteStore

# https://sandbox.evernote.com/api/DeveloperToken.action
dev_token = "<enter your own developer token>"

EN_URL = "https://sandbox.evernote.com"

class EvernoteSession:
    
    def __init__(self, dev_token):
        self.token = dev_token
        self.client = EvernoteClient(token=dev_token)
        self.userStore = self.client.get_user_store()
        self.noteStore = self.client.get_note_store()
        
    def shareSingleNote(self, noteGuid):
        user = self.userStore.getUser()
        shardId = user.shardId
        shareKey = self.noteStore.shareNote(self.token, noteGuid)
        return "%s/shard/%s/sh/%s/%s" % (EN_URL, shardId, noteGuid, shareKey)

    def stopSharingSingleNote(self, noteGuid):
        self.noteStore.stopSharingNote(self.token, noteGuid)
        
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
    
    while 1:
        print
        
        notes = c.listAllNotes()
        for i in range(len(notes)):
            note = notes[i]
            print "[%d] %s (%s)" % (i, note.title, "shared" if note.attributes.shareDate else "private")

        print
        ch = raw_input("Toogle number: ")
        print
        
        if not len(ch):
            break
        
        n = int(ch)        
        note = notes[n]
        
        if not note.attributes.shareDate:
            url = c.shareSingleNote(note.guid)
            print "Sharing note '%s'" % (note.title)
            print "==>", url
            
        else:
            print "Stop sharing note '%s'" % (note.title)
            c.stopSharingSingleNote(note.guid)

