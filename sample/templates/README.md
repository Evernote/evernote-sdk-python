Evernote Giphy
==============
This is a simple application utilizing Flask that serves a random GIF from the Giphy API and then provides you with the option to save it to your Evernote or to go on the the next GIF.

To run this application yourself edit the server.py file and add your consumer key and consumer secret in the corresponding varibles at the begining of the file.  If you do not have a Evernote API key please goto [https://dev.evernote.com#apikey](https://dev.evernote.com#apikey) to get one (for free!).  This application is compatible with Basic, Full and App notebook API keys.

Dependencies
*Evernote
*Flask
*Requests

Then run 

    $python server.py 

from the command line and point your favorite web browser at [localhost:8080](http://localhost:8080/)


