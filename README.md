Evernote SDK for Python 
============================================

Evernote API version 1.23

Overview
--------
This SDK contains wrapper code used to call the Evernote Cloud API from Python.

The SDK also contains a sample script. The code demonstrates the basic use of the SDK for single-user scripts. Real web applications must use OAuth to authenticate to the Evernote service.

Prerequisites
-------------
In order to use the code in this SDK, you need to obtain an API key from http://dev.evernote.com/documentation/cloud. You'll also find full API documentation on that page.

In order to run the sample code, you need a user account on the sandbox service where you will do your development. Sign up for an account at https://sandbox.evernote.com/Registration.action 

In order to run the client client sample code, you need a developer token. Get one at https://sandbox.evernote.com/api/DeveloperToken.action

Getting Started - Client
------------------------
The code in `sample/client/EDAMTest.py` demonstrates the basics of using the Evernote API, using developer tokens to simplify the authentication process while you're learning. 

1. Open `sample/client/EDAMTest.py`
2. Scroll down and fill in your Evernote developer token.
3. On the command line, run the following command to execute the script:

    ```bash
    $ export PYTHONPATH=../lib; python EDAMTest.py
    ```

Getting Started - OAuth
------------------------
Web applications must use OAuth to authenticate to the Evernote service. The code in sample/django contains a simple web apps that demonstrate the OAuth authentication process. The application use the Django framework. You don't need to use Django for your application, but you'll need it to run the sample code.

1. Install `django`, `oauth2` and `evernote` library.  You can also use `requirements.txt` for `pip`.
2. Open the file `oauth/views.py`
3. Fill in your Evernote API consumer key and secret.
4. On the command line, run the following command to start the sample app:

    ```bash
    $ python manage.py runserver
    ```

5. Open the sample app in your browser: `http://localhost:8000`

Usage
-----
### OAuth ###
```python
client = EvernoteOAuth::Client.new(
    consumerKey='YOUR CONSUMER KEY',
    consumerSecret='YOUR CONSUMER SECRET',
    sandbox=True # Default: True
)
requestToken = client.getRequestToken('YOUR CALLBACK URL')
client.getAuthorizeUrl(requestToken)
 => https://sandbox.evernote.com/OAuth.action?oauth_token=OAUTH_TOKEN
```
To obtain the access token
```python
accessToken = client.getAccessToken(
    requestToken['oauth_token'],
    requestToken['oauth_token_secret'],
    request.GET.get('oauth_verifier', '')
)
```
Now you can make other API calls
```python
client = EvernoteClient(token=accessToken)
noteStore = client.getNoteStore()
notebooks = noteStore.listNotebooks()
```

### UserStore ###
Once you acquire token, you can use UserStore. For example, if you want to call UserStore.getUser:
```python
client = EvernoteClient(token=accessToken)
userStore = client.getUserStore()
userStore.getUser()
```
You can omit authenticationToken in the arguments of UserStore functions.

### NoteStore ###
If you want to call NoteStore.listNotebooks:
```python
noteStore = client.getNoteStore()
noteStore.listNotebooks()
```

### NoteStore for linked notebooks ###
If you want to get tags for linked notebooks:
```python
linkedNotebook = noteStore.listLinkedNotebooks()[0]
sharedNoteStore = client.getSharedNoteStore(linkedNotebook)
sharedNotebook = sharedNoteStore.getSharedNotebookByAuth()
sharedNoteStore.listTagsByNotebook(sharedNotebook.notebookGuid)
```

### NoteStore for Business ###
If you want to get the list of notebooks in your business account:
```python
businessNoteStore = client.getBusinessNoteStore()
businessNoteStore.listNotebooks()
```

### References ###
- Evernote Developers: http://dev.evernote.com/
- API Document: http://dev.evernote.com/documentation/reference/
