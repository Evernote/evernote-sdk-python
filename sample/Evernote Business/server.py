# Evernote imports
# for connecting to the Evernote API
import evernote.edam.type.ttypes as Types
# for note, tag, note filter, result spec, and error datatypes
from evernote.api.client import EvernoteClient
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.error.ttypes as Errors

# Flask Imports
from flask import Flask, render_template, request, session, redirect, url_for

# Other Imports
import math
import sys
# to get note thumnails through the HTTP API
import requests
# For URL encoding images
import base64

# API Key information to get a API key go here:
# https://dev.evernote.com#apikey
CONSUMER_KEY = "PUT API KEY HERE"
CONSUMER_SECRET = "PUT API SECRET HERE"
# If True will use sandbox.evernote.com, if False will use www.evernote.com
sandbox = True
if sandbox:
    EN_URL = "https://sandbox.evernote.com"
else:
    EN_URL = "https://www.evernote.com"

# PORT FOR DEVELOPERMENT SERVER
port = 1337

# Throw an error and exit if there is no Consumer key or secret entered
# to get a key go to https://dev.evernote.com#apikey
if CONSUMER_KEY == "PUT API KEY HERE"
or CONSUMER_KEY == ""
or CONSUMER_SECRET == "PUT API SECRET HERE"
or CONSUMER_SECRET == "":
    print """ERROR: Edit the server.py file and add your consumer key \
    and consumer secret in lines 18 an 19 at the begining of \
    "server.py"\nIf you do not have a Evernote consumer key and secret \
    go to https://dev.evernote.com#apikey to get one (for free!).\n"""
    sys.exit(1)

# Start Flask
app = Flask(__name__)
# Configure the secret key for session data (must be the same secret
# key when starting Flask in the last line)
app.config['SECRET_KEY'] = "secret key"


@app.route("/auth")
def auth():
    """Takes a callback for Evernote's OAuth process

    Redirect to main after auth token is retrived/stored in session"""

    # Check to make sure the user approved the appliction
    # (oauth_verifier will not be present if they declined)
    if "oauth_verifier" in request.args:
        # Setup client
        client = EvernoteClient(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            sandbox=sandbox
        )

        # Get access token
        try:
            auth_token = client.get_access_token(
                session['oauth_token'], session['oauth_token_secret'],
                request.args['oauth_verifier']
            )
        except:
            # Display anerror message to the user if unable to
            # authorize Evernote account access
            error_message = "OAuth Error with application '%s'" % CONSUMER_KEY
            return render_template("error.html", error_message=error_message)

        # Attach the user's access token to the session
        session["access_token"] = auth_token

        # Redirect to main
        return redirect(url_for("main"))

    # Display an error to the user when the user doesn't grant access
    # of the application to access their Evernote account
    else:
        error_message = "OAuth Error:\
        Please approve access to the appliction %s" % CONSUMER_KEY
        return render_template("error.html", error_message=error_message)


@app.route("/", methods=['POST', 'GET'])
def main():
    """Presents the user with notes tagged as templates

    If there are no notes tagged "template" or "Template" 4 example
    notes are created. If the user is not logged in: a splash page with
    the option to authorize the appliction is presented. Utilizes
    access tokenk stored in the session.
    """

    # Check to see the user has logged in
    if "access_token" in session.keys():
        try:
            # Setup Evernote client
            client = EvernoteClient(
                token=session["access_token"],
                sandbox=sandbox
            )
            user_store = client.get_user_store()
            note_store = client.get_note_store()
        except Errors.EDAMSystemException:
            # If the user authentication token fails to work
            # prompt them to reautenticate
            error_message = "Your session is no longer valid.  \
            Please click here <a href=\'/clear'>click here</a> \
            to reset and login again."
            return render_template("error.html", error_message=error_message)

        # If the user is not a part of the business, tell the user
        user = user_store.getUser()
        if not user.accounting.businessId:
            error_message = "This account is not a part of a business. \
            Please click here <a href=\'/clear'>click here</a> to reset \
            and try another account."
            return render_template("error.html", error_message=error_message)
        else:
            business_store = client.get_business_note_store()

        # Setup search
        notebook_filter = NoteStoreTypes.NoteFilter()
        result_spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)

        # Start seraching for notes in the last day if less than 5
        # results increase to 10, 100, etc. until more than 5 are found
        # or the number results between iterations are the same
        search_results_len = None
        while search_results_len < 10:
            # Setup counter
            try:
                counter += 1
            except NameError:
                counter = 0

            # Define number of pervious days to search:
            days_pervious_to_search = str(int(math.pow(10, counter)))
            # Define search grammer
            # https://dev.evernote.com/doc/articles/search_grammar.php
            notebook_filter.words = "created:day-%s updated:day-%s" % \
                (days_pervious_to_search, days_pervious_to_search)

            # Execute search method call
            search_results = business_store.findNotesMetadata(
                notebook_filter,
                0,
                40000,
                result_spec
            )

            # Break if you get the same number of results for a order
            # of magnitude increase in the number of days (assume that
            # is the total number of search results present)
            if len(search_results.notes) == search_results_len
            and search_results_len != 0:
                break

            # If you search the last 10,000 days and there are not
            # business notes assume there are no business notes and
            # inform the user
            if counter == 4 and search_results_len == 0:
                error_message = "This account has no business notes! \
                Please click please add and sync some business notes \
                and refresh the page."
                return render_template(
                    "error.html",
                    error_message=error_message
                )

            search_results_len = len(search_results.notes)

        notes_metadata = search_results.notes

        auth_result = user_store.authenticateToBusiness()
        business_shard_id = auth_result.user.shardId
        business_user_id = auth_result.user.id
        business_token = auth_result.authenticationToken

        # Return the list of recently created and edited business notes
        # and their views and display them (with links) to the user
        for note in notes_metadata:
            # Construct a link to the template note with the form
            # evernote:///view/[userId]/[shardId]/[noteGuid]/[noteGuid]
            template_link = "evernote:///view/%s/%s/%s/%s/" % \
                (business_user_id, business_shard_id, note.guid, note.guid)

            # Construct a URL that allows the user to create a new note
            # based on the template
            in_app_link = "note/template/%s" % note.guid

            # Get the thumnail for each note
            thumbnail_url = "%s/shard/%s/thm/note/%s.jpg" % \
                (EN_URL, business_shard_id, note.guid)
            r = requests.post(thumbnail_url, data={"auth": business_token})

            # Base64 encode the image data to return with the page
            # this is to get avoid exposing the business token in
            # plain HTML on the page (which is requried to retrive
            # the image)
            image_data = "data:%s;base64,%s" % (
                r.headers['Content-Type'],
                str(base64.b64encode(r.content).decode("utf-8"))
            )

            # Wrap all this data in a dictionary and put it in a list
            try:
                content_list.append(
                    {"image": image_data,
                        "in_app_link": in_app_link,
                        "title": str(note.title).decode('utf-8')}
                )
            except NameError:
                content_list = [{
                	"image": image_data,
                    "in_app_link": in_app_link,
                    "title": str(note.title).decode('utf-8')
                }]

        # Render the template with the data we just retrivied
        return render_template(
            'index.html',
            templates=content_list,
            num_of_notes=days_pervious_to_search
        )

    # If their Evernote access_token session varible is not set,
    # redirect them to Evernote to authorize the applicaiton
    else:
        # Setup Evernote client
        client = EvernoteClient(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            sandbox=sandbox
        )
        try:
            # Set callback URL
            callback_url = "http://localhost:%d/auth" % port
            request_token = client.get_request_token()
            # Set OAuth token in the broswer session
            session['oauth_token'] = request_token['oauth_token']
            # Set OAuth secret in the broswer session
            session['oauth_token_secret'] = request_token['oauth_token_secret']
            # Get redirect URL
            authorize_url = client.get_authorize_url(request_token)
        except KeyError:
            # If there is an error alert the user
            # and prompt them to reauthenticate
            error_message = "Invalid API key and/or secret. \
            Please verify that the values of CONSUMER_KEY \
            and CONSUMER_SECRET in  lines 18 an 19 of server.py \
            are valid and then <a href=\'/clear'>click here</a> to reset."
            return render_template("error.html", error_message=error_message)
        else:
            # Present the user with a page descibing what the
            # appliction does, and prompt them to authorize the
            # app to access their Evernote account
            return render_template('splash.html', auth_url=authorize_url)


@app.route("/note/template/<guid>")
def new_template_note(guid):
    """Copies the note specified by the GUID in the URL

    redirects the user to open the note in their client"""

    # Check to see the user has logged in
    if "access_token" in session.keys():
        # Setup Evernote Client
        client = EvernoteClient(token=session["access_token"], sandbox=sandbox)
        user_store = client.get_user_store()
        business_store = client.get_business_note_store()

        auth_result = user_store.authenticateToBusiness()
        business_shard_id = auth_result.user.shardId
        business_user_id = auth_result.user.id
        business_token = auth_result.authenticationToken

        # Construct the evernote Link to the newly copied note
        in_app_link = "evernote:///view/%s/%s/%s/%s/" % (
            business_user_id,
            business_shard_id,
            guid,
            guid
        )

        # Redirect the user to the note (opens in Evernote client)
        return redirect(in_app_link)
    else:
        # If the user is not logged in redirect them to do so
        return redirect(url_for("main"))


# Clears session (for debugging/testing)
@app.route("/clear")
def clears():
    """Clears user's session varilbles

    Intended for debugging use"""

    # Remove all the session varibles
    try:
        del session["access_token"]
        del session['oauth_token']
        del session['oauth_token_secret']
    except KeyError:
        pass

    # Indicate to the user the session has been cleared and redirect
    # them (via Javascript) to main
    return render_template("reset.html")

if __name__ == "__main__":
    # Configure the secret key for session data
    app.secret_key = "secret key"
    # Start the app on the localhost in debug mode on the port
    # specified in the begining of this file
    app.run(host='0.0.0.0', debug=True, port=port)
