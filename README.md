Evernote SDK for Python
============================================

Evernote API version 1.28 

This SDK is intended for use with Python 2.X

For Evernote's beta Python 3 SDK see https://github.com/evernote/evernote-sdk-python3

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
    $ export PYTHONPATH=../../lib; python EDAMTest.py
    ```

Getting Started - Django with OAuth
------------------------------------
Web applications must use OAuth to authenticate to the Evernote service. The code in sample/django contains a simple web apps that demonstrate the OAuth authentication process. The application use the Django framework. You don't need to use Django for your application, but you'll need it to run the sample code.

1. Install `django`, `oauth2` and `evernote` library.  You can also use `requirements.txt` for `pip`.
2. Open the file `oauth/views.py`
3. Fill in your Evernote API consumer key and secret.
4. On the command line, run the following command to start the sample app:

    ```bash
    $ python manage.py runserver
    ```

5. Open the sample app in your browser: `http://localhost:8000`

Getting Started - Pyramid with OAuth
-------------------------------------
If you want to use Evernote API with Pyramid, the code in sample/pyramid will be good start.

1. Install the sample project using pip on your command line like this.

    ```bash
    $ pip install -e .
    ```

2. Open the file `development.ini`
3. Fill in your Evernote API consumer key and secret.
4. On the command line, run the following command to start the sample app:

    ```bash
    $ pserve development.ini
    ```

5. Open the sample app in your browser: `http://localhost:6543`


Usage
-----
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
- API Document: http://dev.evernote.com/documentation/reference/


Known Issues
------------
### Regular expressions ###
In general, the ["re" regex module](http://docs.python.org/2/library/re.html) doesn't handle some of our regular expressions in [Limits](https://github.com/evernote/evernote-sdk-python/blob/master/lib/evernote/edam/limits/constants.py), but [re2](https://pypi.python.org/pypi/re2/) does.
