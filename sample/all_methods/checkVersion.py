# Import the Evernote client
from evernote.api.client import EvernoteClient
# Import UserStoreConstants to get version of SDK
import evernote.edam.userstore.constants as UserStoreConstants

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get user store object
user_store = client.get_user_store()

# Call authenticateToBusiness
version_ok = user_store.checkVersion("Evernote Test (Python)", 
	UserStoreConstants.EDAM_VERSION_MAJOR, 
	UserStoreConstants.EDAM_VERSION_MINOR)

if version_ok:
	print "Your Evernote client is compatible with Evernote's current service!"
else:
	print "Your Evernote client is out of date, please upgrade your client"