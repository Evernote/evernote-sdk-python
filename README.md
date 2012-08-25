Evernote SDK for Python 
============================================

Evernote API version 1.22

Overview
--------
This SDK contains wrapper code used to call the Evernote Cloud API from Python.

The SDK also contains a sample script. The code demonstrates the basic use of the SDK for single-user scripts. Real web applications must use OAuth to authenticate to the Evernote service.

Prerequisites
-------------
In order to use the code in this SDK, you need to obtain an API key from http://dev.evernote.com/documentation/cloud. You'll also find full API documentation on that page.

In order to run the sample code, you need a user account on the sandbox service where you will do your development. Sign up for an account at https://sandbox.evernote.com/Registration.action 

In order to run the client client sample code, you need a developer token. Get one at https://sandbox.evernote.com/api/DeveloperToken.action

Getting Started
---------------
The code in sample/client/EDAMTest.py demonstrates the basics of using the Evernote API, using developer tokens to simplify the authentication process while you're learning. 

1. Open sample/client/EDAMTest.py
2. Scroll down and fill in your Evernote developer token.
3. On the command line, run the following command to execute the script:

    export PYTHONPATH=../lib; python EDAMTest.py
