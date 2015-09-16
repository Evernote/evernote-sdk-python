# Import the Evernote client
from evernote.api.client import EvernoteClient
# Import Evernote types to get service level enum (Basic, Plus, Permium)
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get user store object
user_store = client.get_user_store()

# Get user
user = user_store.getUser()

#Map service level enum to desciption string
service_level = Types.ServiceLevel._VALUES_TO_NAMES[user.serviceLevel]

print "%s's user ID is %s." % (user.username, user.id)
print "%s is a %s user." % (user.username, service_level)


if user.accounting.businessId:
	print "%s is a part of the '%s' business!" % (user.username, user.accounting.businessName)



