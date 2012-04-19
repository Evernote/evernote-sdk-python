#
# A simple Evernote API demo application that authenticates with the
# Evernote web service, lists all notebooks in the user's account,
# and creates a simple test note in the default notebook.
#
# Before running this sample, you must change the API consumer key
# and consumer secret to the values that you received from Evernote.
#
# To run (Unix):
#   export PYTHONPATH=../lib; python EDAMTest.py myuser mypass
#

import sys
import hashlib
import binascii
import time
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

# NOTE: Provide the consumer key and consumer secret that you received from Evernote
consumerKey = ""
consumerSecret = ""

if not consumerKey or not consumerSecret:
    print "Please set your API consumer key and secret"
    print "To get an API key, visit http://dev.evernote.com/documentation/cloud/"
    exit(1)
        
if len(sys.argv) < 3:
    print "Arguments:  <username> <password>";
    exit(1)

username = sys.argv[1]
password = sys.argv[2]

evernoteHost = "sandbox.evernote.com"
userStoreUri = "https://" + evernoteHost + "/edam/user"

userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
userStore = UserStore.Client(userStoreProtocol)

versionOK = userStore.checkVersion("Python EDAMTest",
                                   UserStoreConstants.EDAM_VERSION_MAJOR,
                                   UserStoreConstants.EDAM_VERSION_MINOR)

print "Is my EDAM protocol version up to date? ", str(versionOK)
print ""
if not versionOK:
    exit(1)

# Authenticate the user
try :
    authResult = userStore.authenticate(username, password,
                                        consumerKey, consumerSecret)
except Errors.EDAMUserException as e:
    # See http://www.evernote.com/about/developer/api/ref/UserStore.html#Fn_UserStore_authenticate
    parameter = e.parameter
    errorCode = e.errorCode
    errorText = Errors.EDAMErrorCode._VALUES_TO_NAMES[errorCode]
    
    print "Authentication failed (parameter: " + parameter + " errorCode: " + errorText + ")"
    
    if errorCode == Errors.EDAMErrorCode.INVALID_AUTH:
        if parameter == "consumerKey":
            if consumerKey == "en-edamtest":
                print "You must replace the variables consumerKey and consumerSecret with the values you received from Evernote."
            else:
                print "Your consumer key was not accepted by", evernoteHost
                print "This sample client application requires a client API key. If you requested a web service API key, you must authenticate using OAuth."
            print "If you do not have an API Key from Evernote, you can request one from http://dev.evernote.com/documentation/cloud/"
        elif parameter == "username":
            print "You must authenticate using a username and password from", evernoteHost
            if evernoteHost != "www.evernote.com":
                print "Note that your production Evernote account will not work on", evernoteHost
                print "You must register for a separate test account at https://" + evernoteHost + "/Registration.action"
        elif parameter == "password":
            print "The password that you entered is incorrect"

    print ""
    exit(1)

user = authResult.user
authToken = authResult.authenticationToken
print "Authentication was successful for ", user.username
print "Authentication token = ", authToken

noteStoreHttpClient = THttpClient.THttpClient(authResult.noteStoreUrl)
noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
noteStore = NoteStore.Client(noteStoreProtocol)

notebooks = noteStore.listNotebooks(authToken)
print "Found ", len(notebooks), " notebooks:"
for notebook in notebooks:
    print "  * ", notebook.name
    if notebook.defaultNotebook:
        defaultNotebook = notebook

print
print "Creating a new note in default notebook: ", defaultNotebook.name
print

# Create a note with one image resource in it ...

image = open('enlogo.png', 'rb').read()
md5 = hashlib.md5()
md5.update(image)
hash = md5.digest()
hashHex = binascii.hexlify(hash)

data = Types.Data()
data.size = len(image)
data.bodyHash = hash
data.body = image

resource = Types.Resource()
resource.mime = 'image/png'
resource.data = data

note = Types.Note()
note.title = "Test note from EDAMTest.py"
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>Here is the Evernote logo:<br/>'
note.content += '<en-media type="image/png" hash="' + hashHex + '"/>'
note.content += '</en-note>'
note.resources = [ resource ]

createdNote = noteStore.createNote(authToken, note)

print "Successfully created a new note with GUID: ", createdNote.guid
