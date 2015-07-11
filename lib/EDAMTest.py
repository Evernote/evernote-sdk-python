#
# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
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

from evernote.api.client import EvernoteClient

# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit
# https://sandbox.evernote.com/api/DeveloperToken.action
auth_token = "S=s1:U=8fa39:E=1543590664a:C=14cdddf3880:P=1cd:A=en-devtoken:V=2:H=4ca68db61c8ba43420df1b7ba6879fa6"

if auth_token == "your developer token":
    print "Please fill in your developer token"
    print "To get a developer token, visit " \
        "https://sandbox.evernote.com/api/DeveloperToken.action"
    exit(1)

# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and replace your
# developer token above with a token from
# https://www.evernote.com/api/DeveloperToken.action

client = EvernoteClient(token=auth_token, sandbox=True)

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

notebook_share = NoteStoreTypes.ManageNotebookSharesParameters()
notebook_share.membershipsToUpdate = [invite]

notebook_share.inviteMessage = "Hello...Whatisthis?!"
x = note_store.listNotebooks()[0]
print x.name
notebook_share.notebookGuid = x.guid

note_store.manageNotebookShares(notebook_share)




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

    print "Found", len(set(joined_business_notebooks+accessible_business_notebooks))-len(accessible_business_notebooks), "additional business notebooks accessible to you:"
    for accessible_business_notebook in accessible_business_notebooks:
        if accessible_business_notebook.guid not in [joined_business_notebook.guid for joined_business_notebook in joined_business_notebooks]:
            print "  * ", accessible_business_notebook.name
            
            #list all the notes in the accessible business notebook:
            note_filter = NoteStoreTypes.NoteFilter()
            note_filter.notebookGuid = accessible_business_notebook.guid

            result_spec = NoteStoreTypes.NotesMetadataResultSpec()
            result_spec.includeTitle = True
            
            offset = 0
            page_size = 0

            search_results = business_store.findNotesMetadata(note_filter, offset, page_size, result_spec)

            

            print "Found", len(search_results.notes), "notes in", accessible_business_notebook.name
            for note in search_results.notes:
                print "  + ", accessible_business_notebook.name

