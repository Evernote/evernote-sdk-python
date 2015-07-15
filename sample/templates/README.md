Evernote Templates
==================
This application takes all notes in your account with the tag "template" or "Template" and displays the title and tag of the note here. When you click on a template the application creates a new Evernote note and opens it in your local Evernote client for you to work on.

To run this application yourself edit the server.py file and add your consumer key and consumer secret in the corresponding varibles at the begining of the file.  If you do not have a Evernote API key please goto [https://dev.evernote.com#apikey](https://dev.evernote.com#apikey) to get one (for free!).  This application is compatible with Full and App notebook API keys.

Dependencies
*Evernote
*Flask
*Requests

Then run 

    $python server.py 

from the command line and point your favorite web browser at [localhost:8000](http://localhost:8000/)


