Getting Started - Client
========================
The code in `sample/client/EDAMTest.py` demonstrates the basics of using the Evernote API, using developer tokens or OAuth to demonstrate the various authentication processes.  If you are just learning follow the instructions below under "dev_token.py", if you would like to explore the OAuth process scroll down the "oauth.py".

dev_token.py
------------

1. Create a Evernote sandbox account here: https://sandbox.evernote.com/Registration.action 
2. Get a developer token here: https://sandbox.evernote.com/api/DeveloperToken.action
3. Open `sample/client/dev_token.py`
4. Scroll down and fill in your Evernote developer token, retrived in step 2.
3. On the command line, run the following command to execute the script:

    ```bash
    $ export PYTHONPATH=../../lib; python dev_token.py


oauth.py
--------
1. Get an API key by filling out the form here: https://dev.evernote.com/#apikey and make a note of your consumer key and secret
2. Open `sample/client/oauth.py`
3. Scroll down and fill in your consumer key and consumer secret
4. On the command line, run the following command to execute the script:

    ```bash
    $ export PYTHONPATH=../../lib; python oauth.py

5. Login to your Evernote account and approve access to your application when prompted.