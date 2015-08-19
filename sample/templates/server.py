#Evernote imports
from evernote.api.client import EvernoteClient # for connecting to the Evenrote API
import evernote.edam.type.ttypes as Types # for note and tags datatypes types
import evernote.edam.notestore.ttypes as NoteStoreTypes # for note filter and result spec datatypes

#Flask Imports
from flask import Flask, render_template, request, session, redirect, url_for

#Other Imports
import requests # to get note thumnails through the HTTP API 
import sys # to exit if no API key is inputted
import templates_enml # file that has the note template data
import base64 # for URL encoding images

#API Key information
#to get a API key go here: https://dev.evernote.com#apikey
CONSUMER_KEY="INPUT CONSUMER KEY HERE" #INPUT CONSUMER KEY HERE
CONSUMER_SECRET="INPUT CONSUMER SECRET HERE" #INPUT CONSUMER SECRET HERE
sandbox = True #if True will use sandbox.evernote.com, if False will use www.evenrote.com

# PORT FOR DEVELOPERMENT SERVER
port=8000

#if sandbox True will use sandbox.evernote.com, if False will use www.evenrote.com
if sandbox:
	EN_URL="https://sandbox.evernote.com"
else:
	EN_URL="https://www.evernote.com"

#Throw an error and exit if there is no Consumer key or secret entered
# to get a key go to https://dev.evernote.com#apikey
if CONSUMER_KEY=="PUT API KEY HERE" or CONSUMER_KEY=="" or CONSUMER_SECRET=="PUT API SECRET HERE" or CONSUMER_SECRET=="":
	print """ERROR: Edit the server.py file and add your consumer key and consumer secret in the corresponding varibles at the begining of the file.
	\nIf you do not have a Evernote consumer key and secret go to https://dev.evernote.com#apikey to get one (for free!).\n"""
	sys.exit(1)

#Start Flask 
app=Flask(__name__)
app.config['SECRET_KEY'] = "secret key" #configure the secret key for session data

def get_template_tags(auth_token):
	"""finds a tag with the name 'template' or 'Template'

	returns a list of tag GUIDs or None"""

	#setup the Evernote Client
	client = EvernoteClient(token=session["access_token"], sandbox=sandbox)
	user_store = client.get_user_store()
	note_store = client.get_note_store()

	#get a list of tags in the user's account
	tags = note_store.listTags()

	#Check to see if there are tags named 'template' or 'Template' and put them in a list
	template_tags = None
	for tag in tags:
		tag_name = tag.name
		if tag_name == 'template':
			if template_tags:
				template_tags.append(tag.guid)
			else:
				template_tags = [tag.guid]
		if tag_name == 'Template':
			if template_tags:
				template_tags.append(tag.guid)
			else:
				template_tags = [tag.guid]
	
	return template_tags #return a list of tags GUIDs (or None)

def create_standard_templates(auth_token):
	"""takes an auth token and creates templates notes in the users default notebook

	returns a list of the notes created"""

	#setup Evernote client
	client = EvernoteClient(token=auth_token, sandbox=sandbox)
	note_store = client.get_note_store()

	notes=[]
	default_notebook = note_store.getDefaultNotebook()
	template_tags = get_template_tags(auth_token)

	# add all template note ENML from templates_enml.py file
	for template in templates_enml.templates:
		note = Types.Note()			
		note.title = template['title']
		note.content = template['enml']
		note.tagGuids = template_tags
		note.notebooksGuid = default_notebook.guid
		try:
			notes.append(note_store.createNote(note))
		except NameError:
			notes = [note_store.createNote(note)]

	return notes

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
		
		#setup Evernote client
		client = EvernoteClient(token=session["access_token"], sandbox=sandbox)
		user_store = client.get_user_store()
		note_store = client.get_note_store()

		#get a list of tags labeled "template" or "Template"
		template_tags = get_template_tags(session["access_token"])

		#if a "template" or "Template" tag does already exist do a search for notes tagged with "templates"
		if template_tags:
			personal_search_results = []
			for tag in template_tags:
				notebook_filter=NoteStoreTypes.NoteFilter()
				notebook_filter.tagGuids= [tag]
				result_spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)
				personal_search_result = note_store.findNotesMetadata(notebook_filter,0 , 40000, result_spec)

				personal_search_results+=personal_search_result.notes


			metadata_notes_list = personal_search_results

			#if the search returns less than 4 notes create 4 note templates for them:
			if len(metadata_notes_list) < 4:
				standard_template_notes = create_standard_templates(session["access_token"])
				metadata_notes_list += standard_template_notes

		#if there are no tags labeled "template" or "Template" create it and create standard template notes
		if not template_tags:
			template_tags = Types.Tag()
			template_tags.name = "template"
			template_tags = note_store.createTag(template_tags)

			#create 4 note templates for the user:
			metadata_notes_list = create_standard_templates(session["access_token"])

		#return the list of templates and their views and display them (with their links) to the user
		for note in metadata_notes_list:
			#get the user
			user = user_store.getUser()
			#Get the HTML contents of each note: 
			template_link = "evernote:///view/%s/%s/%s/%s/" % (user.id, user.shardId, note.guid, note.guid)
			#edit this template: Link to note "evernote:///view/[userId]/[shardId]/[noteGuid]/[noteGuid]/"

			#create URL that allows the user to create a new note based on the template
			in_app_link = "note/template/%s" % note.guid

			#get the thumnail for each note
			r=requests.post(EN_URL+"/shard/"+user.shardId+"/thm/note/"+note.guid+".jpg", data={"auth":session["access_token"]})
			image_data = "data:"+r.headers['Content-Type'] + ";" +"base64," + str(base64.b64encode(r.content).decode("utf-8"))

			#wrap all this data in a dictionary and put it in a list
			try:
				content_list.append({"image":image_data, "in_app_link":in_app_link, "template_link":template_link, "title":note.title})
			except NameError:
				content_list = [{"image":image_data, "in_app_link":in_app_link, "template_link":template_link, "title":note.title}]

		#render the template with the data we just retrivied
		return render_template('index.html', templates=content_list)


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
			return render_template("error.html", error_message="invalid API key and/or secret.  Please check the values of cosumer_key and sonsumer_secret in the server.py file are valid and <a href=\'/clear'>click here</a> to reset.")
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
		note_store = client.get_note_store()
		
		#get the default notebook
		default_notebook = note_store.getDefaultNotebook()
		
		#copy the note to the default notebook
		note = note_store.copyNote(session['access_token'], guid, default_notebook.guid)

		#Remove "template" and "Template" tags
		for tag in get_template_tags(session['access_token']):
			try:
				note.tagGuids.remove(tag)
			except ValueError:
				pass
		note = note_store.updateNote(note)

		#construct the evernote Link to the newly copied note
		in_app_link = "evernote:///view/%s/%s/%s/%s/" % (user_store.getUser().id, user_store.getUser().shardId, note.guid, note.guid)

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
