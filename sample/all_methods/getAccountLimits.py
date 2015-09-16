# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import Evernote types to get service level enum (Basic, Plus, Permium)
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

#simple function to give human readable byte sizes
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get user store object
user_store = client.get_user_store()

# Get Account Limits for each service level
basic_account_limits = user_store.getAccountLimits(Types.ServiceLevel.BASIC)
plus_account_limits = user_store.getAccountLimits(Types.ServiceLevel.PLUS)
premium_account_limits = user_store.getAccountLimits(Types.ServiceLevel.PREMIUM)

print "The upload limit for an Evernote Basic account is %s" % sizeof_fmt(basic_account_limits.uploadLimit)
print "The upload limit for an Evernote Plus account is %s" % sizeof_fmt(plus_account_limits.uploadLimit)
print "The upload limit for an Evernote Premium account is %s" % sizeof_fmt(premium_account_limits.uploadLimit)