from evernote.api.client import EvernoteClient
import sys

def working(token):
	try:
		c=EvernoteClient(token=token)
		ns=c.get_note_store()
	except:
		print("Unexpected error:", sys.exc_info())
		return False
	else:
		return True

#setup Evernote Client
client=EvernoteClient(token="S=s432:U=489be66:E=1545a0ad962:C=14d0259ad08:P=1cd:A=en-devtoken:V=2:H=e3e3c9ea30c6879c54918794fad333ae", sandbox=False)
#get note store object to call listTags, listTagsByNotebook, and listNotebooks on
note_store=client.get_note_store()
business_store=client.get_business_note_store()



#get a list of all notebooks
notebooks = note_store.listNotebooks()
