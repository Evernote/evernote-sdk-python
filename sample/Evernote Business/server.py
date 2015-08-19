#Evernote imports
from evernote.api.client import EvernoteClient # for connecting to the Evenrote API
import evernote.edam.type.ttypes as Types # for note and tags datatypes types
import evernote.edam.notestore.ttypes as NoteStoreTypes # for note filter and result spec datatypes
import evernote.edam.error.ttypes as Errors # for handeling errors sent from the Evernote Cloud

#Flask Imports
from flask import Flask, render_template, request, session, redirect, url_for

#Other Imports
import requests # to get note thumnails through the HTTP API 
import sys # to exit if no API key is inputted
import base64 # for URL encoding images
import math # for changing the search query

#API Key information
#to get a API key go here: https://dev.evernote.com#apikey
CONSUMER_KEY="PUT API KEY HERE" #INPUT CONSUMER KEY HERE
CONSUMER_SECRET="PUT API SECRET HERE" #INPUT CONSUMER SECRET HERE
sandbox = True #if True will use sandbox.evernote.com, if False will use www.evenrote.com

# PORT FOR DEVELOPERMENT SERVER
port=1337

#if sandbox True will use sandbox.evernote.com, if False will use www.evenrote.com
if sandbox:
	EN_URL="https://sandbox.evernote.com"
else:
	EN_URL="https://www.evernote.com"

#Throw an error and exit if there is no Consumer key or secret entered
# to get a key go to https://dev.evernote.com#apikey
if CONSUMER_KEY=="PUT API KEY HERE" or CONSUMER_KEY=="" or CONSUMER_SECRET=="PUT API SECRET HERE" or CONSUMER_SECRET=="":
	print """ERROR: Edit the server.py file and add your consumer key and consumer secret in lines 18 an 19 at the begining of "server.py".
	\nIf you do not have a Evernote consumer key and secret go to https://dev.evernote.com#apikey to get one (for free!).\n"""
	sys.exit(1)

#Start Flask 
app=Flask(__name__)
app.config['SECRET_KEY'] = "secret key" #configure the secret key for session data (must be the same secret key when starting Flask in the last line)

@app.route("/auth")
def auth():
	"""Takes a callback for Evernote's OAuth process 

	Redirect to main after login is confirmed an token is stored in the session"""
	
	#check to make sure the user approved the appliction (oauth_verifier will not be present if they declined)
	if "oauth_verifier" in request.args:
		#setup client
		client = EvernoteClient(
		consumer_key=CONSUMER_KEY,
		consumer_secret=CONSUMER_SECRET,
		sandbox= sandbox
		)
		
		#get access token
		try:
			auth_token = client.get_access_token(session['oauth_token'], session['oauth_token_secret'], request.args['oauth_verifier'])
		except:
			return render_template("error.html", error_message="OAuth Error: Please approve access to the appliction %s" % CONSUMER_KEY)	
		
		#attach the user's access token to the session
		session["access_token"]=auth_token

		#redirect to main
		return redirect(url_for("main"))
	
	#If the user did not approve access to our application let the user know
	else:
		return render_template("error.html", error_message="OAuth Error: Please approve access to the appliction %s" % CONSUMER_KEY)


@app.route("/", methods=['POST','GET'])
def main():
	"""Takes the access token in the session and presents the user with notes that are tagged "template" or "Template" 

	If there are no notes tagged "template" or "Template" 4 example notes are created

	If the user is not logged in: a splash page with the option to authorize the appliction is presented
	"""

	#check to see the user has logged in
	if "access_token" in session.keys():
		
		try:
			#setup Evernote client
			client = EvernoteClient(token=session["access_token"], sandbox=sandbox)
			user_store = client.get_user_store()
			note_store = client.get_note_store()			
		except Errors.EDAMSystemException:
			#if the user authentication token fails to work prompt them to reautenticate
			return render_template("error.html", error_message="Your session is no longer valid.  Please click here <a href=\'/clear'>click here</a> to reset and login again.")

		#if the user is not a part of the business, tell the user
		user = user_store.getUser()
		if not user.accounting.businessId:
			return render_template("error.html", error_message="This account is not a part of a business.  Please click here <a href=\'/clear'>click here</a> to reset and try another account.")
		else:
			business_store = client.get_business_note_store()

		#setup search
		notebook_filter=NoteStoreTypes.NoteFilter()
		result_spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)

		# Start seraching for notes in the last day
		# if less than 5 results increase to 10, 100, etc. until more than 5 are found or 
		# the number results between iterations are the same
		search_results_len = None
		while search_results_len<10:
			#setup counter
			try:
				counter += 1
			except NameError:
				counter = 0
			#define number of pervious days to search:
			days_pervious_to_search = str(int(math.pow(10, counter)))
			#Define search grammer (docs: https://dev.evernote.com/doc/articles/search_grammar.php)
			notebook_filter.words = "created:day-"+days_pervious_to_search+" updated:day-"+days_pervious_to_search

			#perform search
			search_results = business_store.findNotesMetadata(notebook_filter,0 , 40000, result_spec)
			
			#break if you get the same number of results for a order of magnitude increase in the number of days
			# (assume that is the total number of search results present)
			if len(search_results.notes)==search_results_len and search_results_len != 0:
				break

			# if you search the last 10,000 days and there are not business notes
			# assume there are no business notes and inform the user
			if counter == 4 and search_results_len==0:
				return render_template("error.html", error_message="This account has no business notes!  Please click please add and sync some business notes and refresh the page.")

			search_results_len = len(search_results.notes)

		notes_metadata = search_results.notes

		auth_result = user_store.authenticateToBusiness()
		business_shard_id = auth_result.user.shardId
		business_user_id = auth_result.user.id
		business_token = auth_result.authenticationToken

		#return the list of recently created and edited business notes and their views and display them (with their links) to the user
		for note in notes_metadata:
			#Get the HTML contents of each note: evernote:///view/32687061/s12/ff36290-4c35-4938-ab73-c09ce4a83e1c/ff36290-4c35-4938-ab73-c09ce4a83e1c/
			template_link = "evernote:///view/%s/%s/%s/%s/" % (business_user_id, business_shard_id, note.guid, note.guid)
			#edit this template: Link to note "evernote:///view/[userId]/[shardId]/[noteGuid]/[noteGuid]/"

			#create URL that allows the user to create a new note based on the template
			in_app_link = "note/template/%s" % note.guid

			#get the thumnail for each note
			r=requests.post(EN_URL+"/shard/"+business_shard_id+"/thm/note/"+note.guid+".jpg", data={"auth":business_token})
			image_data = "data:"+r.headers['Content-Type'] + ";" +"base64," + str(base64.b64encode(r.content).decode("utf-8"))

			#wrap all this data in a dictionary and put it in a list
			try:
				content_list.append({"image":image_data, "in_app_link":in_app_link, "title":str(note.title).decode('utf-8')})
			except NameError:
				content_list = [{"image":image_data, "in_app_link":in_app_link, "title":str(note.title).decode('utf-8')}]
		
		#render the template with the data we just retrivied
		return render_template('index.html', templates=content_list, num_of_notes = days_pervious_to_search)


	#if their Evernote access_token session varible is not set, redirect them to Evernote to authoirze the applicaiton
	else:
		#Setup Evernote client
		client = EvernoteClient(
			consumer_key=CONSUMER_KEY,
			consumer_secret=CONSUMER_SECRET,
			sandbox= sandbox
			)
		try:
			request_token = client.get_request_token("http://localhost:"+str(port)+"/auth") #set callback URL
			session['oauth_token'] = request_token['oauth_token'] #Set OAuth token in the broswer session
			session['oauth_token_secret'] = request_token['oauth_token_secret'] #Set OAuth secret in the broswer session
			authorize_url = client.get_authorize_url(request_token) #get redirect URL
		except KeyError:
			#If there is an error alert the user and prompt them to reauthenticate
			return render_template("error.html", error_message="Invalid API key and/or secret.  Please verify that the values of CONSUMER_KEY and CONSUMER_SECRET in  lines 18 an 19 of server.py are valid and then <a href=\'/clear'>click here</a> to reset.")
		else:
			#Present the user with a page descibing what the appliction does, and prompt them to authorize the app to access their Evernote account
			return render_template('splash.html', auth_url = authorize_url) #suggest notebook name of giphy to user

@app.route("/note/template/<guid>")
def new_template_note(guid):
	"""Copies the note specified by the GUID in the URL

	redirects the user to open the note in their client"""

	#check to see the user has logged in
	if "access_token" in session.keys():
		#setup Evernote Client
		client = EvernoteClient(token=session["access_token"], sandbox=sandbox)
		user_store = client.get_user_store()
		business_store = client.get_business_note_store()
		
		auth_result = user_store.authenticateToBusiness()
		business_shard_id = auth_result.user.shardId
		business_user_id = auth_result.user.id
		business_token = auth_result.authenticationToken

		#construct the evernote Link to the newly copied note
		in_app_link = "evernote:///view/%s/%s/%s/%s/" % (business_user_id, business_shard_id, guid, guid)

		#redirect the user to the note (will open up in Evernote client)
		return redirect(in_app_link)
	else:
		#if the user is not logged in redirect them to do so
		return redirect(url_for("main")) 

#for debugging
@app.route("/clear")
def clears():
	"""Clears user's session varilbles 

	Intended for debugging use"""

	#Remove all the session varibles
	try:
		del session["access_token"]
		del session['oauth_token']
		del session['oauth_token_secret']
	except KeyError:
		pass

	#Indicate to the user the session has been cleared and redirect them (via Javascript) to main
	return render_template("reset.html")

if __name__=="__main__":
	app.secret_key="secret key" #configure the secret key for session data
	app.run(host='0.0.0.0', debug=True, port=port) #Start the app on the localhost in debug mode on the port specified in the begining of this file
