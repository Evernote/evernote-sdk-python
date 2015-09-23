Evernote SDK for Python
============================================

Evernote API version 1.28

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


Usage
-----
There are two ways to authenticate to the Evernote API, developer tokens and OAuth. Developer tokens provide instant access to your Evernote account via the API. For public applications, use of webhook notifications, and advanced permissions we recommend using OAuth.

### OAuth ###
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
### Developer Tokens ###
For testing or just to get you appliction up and running quickly you can get a developer token which works similarly to a OAuth access token for you account.  To learn more about developer tokens go to https://dev.evernote.com/doc/articles/dev_tokens.php

Now you can make other API calls
```python
client = EvernoteClient(token=access_token)
note_store = client.get_note_store()
notebooks = note_store.listNotebooks()
```

### UserStore ###
Once you acquire token, you can use UserStore. For example, if you want to call UserStore.getUser:
```python
client = EvernoteClient(token=access_token)
user_store = client.get_user_store()
user_store.getUser()
```
You can omit authenticationToken in the arguments of UserStore functions.

### NoteStore ###
If you want to call NoteStore.listNotebooks:
```python
note_store = client.get_note_store()
note_store.listNotebooks()
```

### NoteStore for linked notebooks ###
If you want to get tags for linked notebooks:
```python
linked_notebook = note_store.listLinkedNotebooks()[0]
shared_note_store = client.getSharedNoteStore(linked_notebook)
shared_notebook = shared_note_store.getSharedNotebookByAuth()
shared_note_store.listTagsByNotebook(shared_notebook.notebookGuid)
```

### NoteStore for Business ###
If you want to get the list of notebooks in your business account:
```python
business_note_store = client.get_business_note_store()
business_note_store.listNotebooks()
```

### References ###
- Evernote Developers: http://dev.evernote.com/
- API Reference: https://dev.evernote.com/doc/reference/
