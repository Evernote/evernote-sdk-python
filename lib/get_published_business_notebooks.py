token = "S=s1:U=8fa39:E=1543590664a:C=14cdddf3880:P=1cd:A=en-devtoken:V=2:H=4ca68db61c8ba43420df1b7ba6879fa6"

from evernote.api.client import EvernoteClient as ec
import evernote.edam.type.ttypes as Types
from evernote.edam.type.ttypes import SharedNotebookRecipientSettings
import evernote.edam.notestore.ttypes as NoteStoreTypes	

c=ec(token=token, sandbox=True)

ns=c.get_note_store()
us=c.get_user_store()
bs=c.get_business_note_store()


u=us.getUser()
abn = bs.listAccessibleBusinessNotebooks()
# sbn = bs.listSharedNotebooks()
# print u.id
# for name in sbn:
# 	print name
# lnb = Types.LinkedNotebook()
# lnb.shareKey = sbn[0].shareKey
# lnb.shareName = "yes yes real"
# lnb.username = u.username
# lnb.shardId = "s1"
# ns.createLinkedNotebook(lnb)	

for notebook in abn:
	print notebook.name
	if notebook.name == "yes way":
		notebook_selected =notebook

notebook = notebook_selected

#notebook.sharedNotebookIds.append(588345)
notebook.contact.username = u.username
print notebook.sharedNotebooks
notebook.sharedNotebooks = None

bs.updateNotebook(notebook)





for notebook in abn:
	print notebook.name
	if notebook.name == "yes way":
		notebook_selected =notebook

notebook = notebook_selected

print "NOTBOOK BEFORE"
print notebook

shared = Types.SharedNotebook(username=None, sharerUserId=588345, serviceAssigned=1422483362000, globalId='7237-s1', requireLogin=True, userId=590769, allowPreview=False, notebookModifiable=True, notebookGuid='0ca1a07c-01da-4b89-a49c-9718748d86b5', email='mcarroll+test@evernote.com', serviceUpdated=1433797597000, recipientUserId=588345, recipientUsername=None, recipientSettings=SharedNotebookRecipientSettings(reminderNotifyEmail=None, reminderNotifyInApp=None), privilege=5, serviceCreated=1422483362000, id=29239, recipientIdentityId=None)

notebook.sharedNotebooks = [shared]

notebook = bs.updateNotebook(notebook)

for notebook in abn:
	print notebook.name
	if notebook.name == "yes way":
		notebook_selected =notebook

notebook = notebook_selected

print "NOTBOOK after"
print notebook

sn = ns.listSharedNotebooks()
for snbx in sn:
	print snbx.name

# note = Types.Note()
# note.title = "Test note from EDAMTest.py"
# note.content = '<?xml version="1.0" encoding="UTF-8"?>'
# note.content += '<!DOCTYPE en-note SYSTEM ' \
#     '"http://xml.evernote.com/pub/enml2.dtd">'
# note.content += '<en-note>Here is the Evernote!	<br/>'
# note.content += '</en-note>'
# note.notebookGuid = notebook_selected.guid

# print bs.createNote(note)

# #get all notes form notebook
# notebook_filter=NoteStoreTypes.NoteFilter()
# notebook_filter.guid=notebook_selected.guid
# result_spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)
# results    = bs.findNotesMetadata(notebook_filter,0 , 40000, result_spec)
# noteList = results.notes

# for note in noteList:
# 	print note.title

#print bs.updateNotebook(notebook_selected)


