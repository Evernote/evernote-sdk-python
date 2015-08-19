#
# A simple Evernote API demo script that lists all notebooks in the user's
# account all the notes in the user's default notebook, creates a simple
# test note in the default notebook, and lists joined and unjoin accessible
# buiness notebooks in the Business accont (if applicable)
#
# Before running this sample, you must fill in your Evernote developer token.
#
# To run (Unix):
#   export PYTHONPATH=../../lib; python EDAMTest.py
#

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStoreTypes
import sys

from evernote.api.client import EvernoteClient

# Real applications authenticate with Evernote using OAuth
# to get an API key and secret visit
# https://dev.evernote.com/#apikey
CONSUMER_KEY="internal-dev" #INPUT CONSUMER KEY HERE
CONSUMER_SECRET="platform123" #INPUT CONSUMER SECRET HERE
sandbox = True #if True will use sandbox.evernote.com, if False will use www.evenrote.com

#if sandbox True will use sandbox.evernote.com, if False will use www.evenrote.com
if sandbox:
    EN_URL="https://sandbox.evernote.com"
else:
    EN_URL="https://www.evernote.com"

#Throw an error and exit if there is no Consumer key or secret entered
# to get a key go to https://dev.evernote.com#apikey
if CONSUMER_KEY=="PUT API KEY HERE" or CONSUMER_KEY=="" or CONSUMER_SECRET=="PUT API SECRET HERE" or CONSUMER_SECRET=="":
    print """ERROR: Edit the server.py file and add your consumer key and consumer secret in lines 24 and 25 at the begining of "oauth.py".
    \nIf you do not have a Evernote consumer key and secret go to https://dev.evernote.com#apikey to get one (for free!).\n"""
    sys.exit(1)


# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and request your API be approved for access 
# on Evernote's production service 

#setup client
client = EvernoteClient(
consumer_key=CONSUMER_KEY,
consumer_secret=CONSUMER_SECRET,
sandbox= sandbox
)

request_token = client.get_request_token("http://evernote") #set callback URL
try:
    oauth_token = request_token['oauth_token'] #set temporary oauth token
    oauth_token_secret = request_token['oauth_token_secret'] # set temporary oaut token secret
    authorize_url = client.get_authorize_url(request_token) #get redirect URL
except KeyError:
    print "Incorrect consumer key or secret.  Please enter a valid consumer key and secret and try again.  \n\nPlease note that key must be approved to be used on www.evernote.com while all new keys are active by default on sandbox.evernote.com\n\n"
    sys.exit(1)    


print "Please complete the following steps to continue: "
print "(1) Go to: " + authorize_url
print "(2) Grant access to your application"
print "(3) Look at the URL you are directed to and find the string after '&oauth_verifier=' and before '&sandbox_lnb'"
oauth_verifier = raw_input("(4) Enter that string (the OAuth verifier) here: ")

auth_token=None

#get access token
while not auth_token:
    try:
        auth_token = client.get_access_token(oauth_token, oauth_token_secret, oauth_verifier)
    except:
        oauth_verifier = raw_input("Incorrect OAuth verifier.\nTry again or press control+Z to exit.\nOAuthVerifier: ")        

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print "Is my Evernote API version up to date? ", str(version_ok)
print ""
if not version_ok:
    exit(1)



user = user_store.getUser()
 
print "Your username is %s" % user.username
print "Your ID is %s" % user.id

note_store = client.get_note_store()

# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print "Found ", len(notebooks), " notebooks:"
for notebook in notebooks:
    print "  * ", notebook.name

#list all the notes in the default notebook:
default_notebook = note_store.getDefaultNotebook()

#setup search criteria
note_filter = NoteStoreTypes.NoteFilter()
note_filter.notebookGuid = default_notebook.guid
result_spec = NoteStoreTypes.NotesMetadataResultSpec()
result_spec.includeTitle = True
offset = 0
max_notes = 20

#perform search
search_results = note_store.findNotesMetadata(note_filter, offset, max_notes, result_spec)

#display search results if there are results:
if len(search_results.notes) != 0:
    print "\nFound", len(search_results.notes), "notes in the default notebook,", default_notebook.name
    for note in search_results.notes:
        print "\t+ ", note.title

print "\nCreating a new note in the default notebook"

# To create a new note, simply create a new Note object and fill in
# attributes such as the note's title.
note = Types.Note()
note.title = "Test note from EDAMTest.py"

# To include an attachment such as an image in a note, first create a Resource
# for the attachment. At a minimum, the Resource contains the binary attachment
# data, an MD5 hash of the binary data, and the attachment MIME type.
# It can also include attributes such as filename and location.
image = open('enlogo.png', 'rb').read()
md5 = hashlib.md5()
md5.update(image)
hash = md5.digest()

data = Types.Data()
data.size = len(image)
data.bodyHash = hash
data.body = image

resource = Types.Resource()
resource.mime = 'image/png'
resource.data = data

# Now, add the new Resource to the note's list of resources
note.resources = [resource]

# To display the Resource as part of the note's content, include an <en-media>
# tag in the note's ENML content. The en-media tag identifies the corresponding
# Resource using the MD5 hash.
hash_hex = binascii.hexlify(hash)

# The content of an Evernote note is represented using Evernote Markup Language
# (ENML). The full ENML specification can be found in the Evernote API Overview
# at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM ' \
    '"http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>Here is the Evernote logo:<br/>'
note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
note.content += '</en-note>'

# Finally, send the new note to Evernote using the createNote method
# The new Note object that is returned will contain server-generated
# attributes such as the new note's unique GUID.
created_note = note_store.createNote(note)

print "Successfully created a new note with GUID: %s\n" %created_note.guid

#Share notebook
user_identity = Types.UserIdentity()
user_identity.type = Types.UserIdentityType.EMAIL
user_identity.stringIdentifier = "mcarroll+spam117@evernote.com"

invite = NoteStoreTypes.InvitationShareRelationship()
invite.recipientUserIdentity = user_identity
invite.displayName = "Look at my notebook!"
invite.privilege = NoteStoreTypes.ShareRelationshipPrivilegeLevel.FULL_ACCESS
invite.allowPreview = True
sharerUserId = user.id


# Evernote Business 
# To learn more about Evernote Business see https://evernote.com/business
# For Evernote Business documentation see https://dev.evernote.com/doc/articles/business.php

# Check to see if the user is a part of a Evernote Business account
if user.accounting.businessId:
    # we're part of a business
    print "You have Evernote Business!"
    print "Business Name: %s\n" % user.accounting.businessName

    business_store = client.get_business_note_store()

    # List all of the notebooks in the business' account
    joined_business_notebooks = business_store.listNotebooks()
    print "Found", len(joined_business_notebooks), "joined business notebooks:"
    for business_notebook in joined_business_notebooks:
        print "  * ", business_notebook.name
    print ""

    accessible_business_notebooks = business_store.listAccessibleBusinessNotebooks()
    
    num_of_unjoin_business_notebooks = len(accessible_business_notebooks)-len(joined_business_notebooks)

    print "Found " + str(num_of_unjoin_business_notebooks) + " additional business notebooks accessible to you:"
    for accessible_business_notebook in accessible_business_notebooks:
        if accessible_business_notebook.guid not in [joined_business_notebook.guid for joined_business_notebook in joined_business_notebooks]:
            print "  * ", accessible_business_notebook.name
else:
    print "You don't have Evernote Business :("