# Import the Evernote client
from evernote.api.client import EvernoteClient
# Import Evernote types to get service level enum (Basic, Plus, Permium)
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "S=s432:U=489be66:E=157102e2801:C=14fb87cf890:P=1cd:A=en-devtoken:V=2:H=96163d26aad2909ebffdbf1ab0f01997"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = False)

# Get user store object
user_store = client.get_user_store()

# Get public user info
username = "sethdemo"

public_user_info = user_store.getPublicUserInfo(username)

service_level = Types.ServiceLevel._VALUES_TO_NAMES[public_user_info.serviceLevel]
user_id = public_user_info.userId
note_store_url = public_user_info.noteStoreUrl

print "%s's user ID is %s" % (username, user_id)
print "%s is a %s user whose personal note store URL is %s" % (username, service_level, note_store_url)
