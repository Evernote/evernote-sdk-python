#
# A simple Evernote API demo script that lists all notebooks in the
# user's account all the notes in the user's default notebook, creates
# a simple test note in the default notebook, and lists joined and
# unjoin accessible buiness notebooks in the Business account
# (if present)
#
# Before running this sample, you must fill in your Evernote developer
# token or API key.
#
# To run (Unix):
#   export PYTHONPATH=../../lib; python EDAMTest.py
#

# Standard Library Imports for hashing resources
import hashlib
import binascii

# Evernote datatype imports
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStoreTypes

# Evernote client imports
from evernote.api.client import EvernoteClient

#######################################################################
# Before running this sample, you must fill in your Evernote developer
# token or API key.
#######################################################################

# Developer Token
auth_token = "your developer token"

# OR API Key
CONSUMER_KEY = "INPUT CONSUMER KEY HERE"
CONSUMER_SECRET = "INPUT CONSUMER SECRET HERE"

# Initial development shoudl be performed on Evernote's sandbox
# development server. To use the production service, change
# sandbox=False and replace your developer token above with a token
# from  https://www.evernote.com/api/DeveloperToken.action to work with
# a production developer token, avalible at
# https://sandbox.evernote.com/api/DeveloperToken.action
# or a production API key (request your sandbox API key be moved to
# production here: https://dev.evernote.com/support) change the
# following value to "False" if True will use sandbox.evernote.com,
# if False will use www.evenrote.com
sandbox = True


# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that
# allows you to access your own Evernote account. To get a developer
# token, visit https://sandbox.evernote.com/api/DeveloperToken.action
# to get an API key and secret visit https://dev.evernote.com/#apikey

# If no developer token or API is defined alert the user and quit
if auth_token == "your developer token"
and CONSUMER_KEY == "INPUT CONSUMER KEY HERE"
and CONSUMER_SECRET == "INPUT CONSUMER SECRET HERE":
    print "Please fill in your developer token or API Key and secret"
    print "To get a developer token, visit " \
        "https://sandbox.evernote.com/api/DeveloperToken.action" \
        "\nto get a API key and secret please visit" \
        "https://dev.evernote.com/#apikey"
    exit(1)

# If the user provides both default to developer token
elif auth_token != "your devleoper token":
    client = EvernoteClient(token=auth_token, sandbox=sandbox)

# When a API key and secret is provided (and not a developer token)
# use the key and secret  to generate a Evernote client object
elif CONSUMER_KEY != "INPUT CONSUMER KEY HERE"
and CONSUMER_SECRET != "INPUT CONSUMER SECRET HERE":
    # Setup client
    client = EvernoteClient(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        sandbox=sandbox
    )

    # Set callback URL
    request_token = client.get_request_token("http://evernote")
    try:
        # Set temporary oauth token
        temp_token = request_token['oauth_token']
        # Set temporary OAuth secret
        temp_secret = request_token['oauth_token_secret']
        # Get redirect URL
        auth_url = client.get_authorize_url(request_token)
    except KeyError:
        print "Incorrect consumer key or secret."
        print "Please enter a valid consumer key and secret and try again."
        print ""
        print "All new keys are active by default on sandbox.evernote.com"
        print "Keys must be approved to be used on www.evernote.com"
        print ""
        sys.exit(1)

    print "Please complete the following steps to continue: "
    print "1. Go to: %s" % auth_url
    print "2. Grant access to your application"
    print "3. Inspect at the URL you are directed to"
    print "4. Find the code in between '&oauth_verifier=' and '&sandbox_lnb'"
    print "5. Enter that code (the OAuth verifier) below: "
    verifier = raw_input("OAuth verifier: ")

    auth_token = None

    # Get access token
    while not auth_token:
        try:
            auth_token = client.get_access_token(
                temp_token,
                temp_secret,
                verifier
            )
        except:
            print "Incorrect OAuth verifier."
            print "Try again or press control+Z to exit."
            verifier = raw_input("OAuthVerifier: ")

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

# List all the notes in the default notebook:
default_notebook = note_store.getDefaultNotebook()

# Setup search criteria
note_filter = NoteStoreTypes.NoteFilter()
note_filter.notebookGuid = default_notebook.guid
spec = NoteStoreTypes.NotesMetadataResultSpec()
spec.includeTitle = True
offset = 0
max_notes = 20

# Perform search
results = note_store.findNotesMetadata(note_filter, offset, max_notes, spec)

# Display search results if there are results:
if len(results.notes) != 0:
    print "\nFound %d notes in the default notebook %s" \
        % (len(results.notes), default_notebook.name)
    for note in results.notes:
        print "\t+ ", note.title

print "\nCreating a new note in the default notebook"

# To create a new note, simply create a new Note object and fill in
# attributes such as the note's title.
note = Types.Note()
note.title = "Test note from EDAMTest.py"

# To include an attachment such as an image in a note, first create a
# resource for the attachment. At a minimum, the Resource contains the
# binary attachment data, an MD5 hash of the binary data, and the
# attachment MIME type. It can also include attributes such as filename
# and location.
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

# To display the Resource as part of the note's content, include an
# <en-media> tag in the note's ENML content. The en-media tag
# identifies the corresponding resource using the MD5 hash.
hash_hex = binascii.hexlify(hash)

# The content of an Evernote note is represented using Evernote Markup
# Language (ENML). The full ENML specification can be found in the
# Evernote API Overview at
# http://dev.evernote.com/documentation/cloud/chapters/ENML.php
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

print "Successfully created a new note with GUID: %s\n" % created_note.guid


# Evernote Business
# To learn more about Evernote Business see https://evernote.com/business
# For Evernote Business documentation see
# https://dev.evernote.com/doc/articles/business.php

# Check to see if the user is a part of a Evernote Business account
if user.accounting.businessId:
    # we're part of a business
    print "You have Evernote Business!"
    print "Business Name: %s\n" % user.accounting.businessName

    business_store = client.get_business_note_store()

    # List all of the notebooks in the business' account
    joined_b_ntbks = business_store.listNotebooks()
    joined_b_ntbk_guids = []
    print "Found", len(joined_b_notebooks), "joined business notebooks:"
    for business_notebook in joined_b_ntbks:
        print "  * ", business_notebook.name
        joined_b_ntbk_guids.append(business_notebook.guid)
    print ""

    # Get a list of accessible business notebooks
    accessible_b_ntbks = business_store.listAccessibleBusinessNotebooks()

    # Infer the list of unjoin business notebooks
    unjoined_b_ntbks = list(set(accessible_b_ntbks)-set(joined_b_ntbks))

    # Print the results to the user
    print "Found %d additional business notebooks accessible to you:" % \
        len(num_unjoined_biz_ntbk)
    for accessible_business_notebook in accessible_business_notebooks:
        if accessible_business_notebook.guid not in join_b_ntbk_guids:
            print "  * ", accessible_business_notebook.name
else:
    print "You don't have Evernote Business"
