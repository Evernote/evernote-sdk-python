Evernote SDK for Python
============================================

Evernote API version 1.28

This SDK is intended for use with Python 2.X

[Getting Started Guide](https://www.evernote.com/l/AAx5Wy2HPa9JqakerbR1mmK9QbCMzSlBfz8)

Overview
--------
This SDK contains wrapper code used to call the Evernote Cloud API from Python.

The SDK also contains sample scripts and demos. These examples demonstrate the basic use of the SDK for single-user scripts as well as OAuth for multiuser applictions. Applications deployed to users are expected to use OAuth to authenticate to the Evernote service.

Prerequisites
-------------
In order to run the sample code and demos in this SDK you will need a Evernote sandbox account and either a API key and secret or a developer token.  To get a user account on Evernote's sandbox service where you will do your development, sign up for an account at https://sandbox.evernote.com/Registration.action

*	Obtian an API key and secret

Go to http://dev.evernote.com/#apikey and fill out the form to get an API key and secret.

* How to get a developer token

In order to run some of the sample code, you need a developer token. Get one at https://sandbox.evernote.com/api/DeveloperToken.action


Authentication
--------------
There are two ways to authenticate to the Evernote API, developer tokens and OAuth. Developer tokens provide instant access to your Evernote account via the API. For public applications, use of webhook notifications, and advanced permissions we recommend using OAuth.

##### OAuth #####
```python
client = EvernoteClient(
    consumer_key='YOUR CONSUMER KEY',
    consumer_secret='YOUR CONSUMER SECRET',
    sandbox=True # Default: True
)
request_token = client.get_request_token('YOUR CALLBACK URL')
client.get_authorize_url(request_token)
 => https://sandbox.evernote.com/OAuth.action?oauth_token=OAUTH_TOKEN
```
To obtain the access token
```python
access_token = client.get_access_token(
    request_token['oauth_token'],
    request_token['oauth_token_secret'],
    request.GET.get('oauth_verifier', '')
)
```
##### Developer Tokens #####
For testing or just to get you appliction up and running quickly you can get a developer token which works similarly to a OAuth access token for you account.  To learn more about developer tokens go to https://dev.evernote.com/doc/articles/dev_tokens.php

Now you can make other API calls
```python
client = EvernoteClient(token=access_token)
note_store = client.get_note_store()
notebooks = note_store.listNotebooks()
```

Usage
-----
Once you have a developer or access token you can access Evernote through the API on behalf of a user (or yourself!).  There are two main structures avalible to access Evernote data throught the API, the UserStore and NoteStore.  The UserStore is the container for accessing and calling methods related to user information while the NoteStore is a contianer for accessing and calling methods related to notes, file attachments, pictures, note content, note metadata, notebooks, stacks and anything related to note storage.

##### UserStore #####
Once you acquire token, you can use UserStore. For example, if you want to call UserStore.getUser:
```python
client = EvernoteClient(token=access_token)
user_store = client.get_user_store()
user_store.getUser()
```
You can omit authenticationToken in the arguments of UserStore functions.

##### NoteStore #####
If you want to call NoteStore.listNotebooks:
```python
note_store = client.get_note_store()
note_store.listNotebooks()
```

##### NoteStore for Business #####
If a user is a part of a Evernote Business account you also have access to the users Evernote Business note store which contians notes owed by the business that are accessiable to the user you are acting on behalf of.  Once you get the business note store object it behaves in a similar fasion to personal note stores
```python
business_note_store = client.get_business_note_store()
business_note_store.listNotebooks()
```

Next Steps
----------
Now you can take a look at the code in the "sample" folder.  There are serveral examples including:
* Sample code for every method in the folder "all_methods"
* An examples of a Evernote Business application in "Evernote Business"
* A test script in "client"
* A web application that saves random GIFs to Evernote in "giphy"
* A web application that makes and serves Evernote template notes in "templates"


### References ###
- Evernote Developers: http://dev.evernote.com/
- API Reference: https://dev.evernote.com/doc/reference/
