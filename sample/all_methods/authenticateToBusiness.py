# Import the Evernote client
from evernote.api.client import EvernoteClient

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get user store object
user_store = client.get_user_store()

# Call authenticateToBusiness
business_authentication_result = user_store.authenticateToBusiness()

business_authentication_token = business_authentication_result.authenticationToken
business_note_store_url = business_authentication_result.noteStoreUrl

print "The business authentication token is: \n\n    %s\n " % business_authentication_token
print "and the business note store URL is \n\n    %s" % business_note_store_url

print "\nYou can use the above note store URL and business authentication token to access the business note store on behalf of the user!"
print "For more information see https://dev.evernote.com/doc/articles/business.php"