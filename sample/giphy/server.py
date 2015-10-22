#Evernote imports
from evernote.api.client import EvernoteClient # for connecting to the Evenrote API
import evernote.edam.type.ttypes as Types # for note and tags datatypes types
import evernote.edam.notestore.ttypes as NoteStoreTypes # for note filter and result spec datatypes
import evernote.edam.error.ttypes as Errors # For Evernote error handling

#Flask Imports
from flask import Flask, render_template, request, session, redirect, url_for

#Other Imports
import requests #for getting Giphy images
import sys # to exit if no API key is inputted
import binascii #for taking the hash of the files for Evernote upload
import hashlib #for taking the hash of the files for Evernote upload
import json #for handling Giphy data

#Giphy public beta API key
giphy_api_key="dc6zaTOxFJmzC" #public beta key

#API Key information
#to get a API key go here: https://dev.evernote.com#apikey
CONSUMER_KEY="INPUT CONSUMER KEY HERE" #INPUT CONSUMER KEY HERE
CONSUMER_SECRET="INPUT CONSUMER SECRET HERE" #INPUT CONSUMER SECRET HERE
sandbox = True #if True will use sandbox.evernote.com, if False will use www.evenrote.com

# PORT FOR DEVELOPERMENT SERVER
port=8080

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
app.config['SECRET_KEY'] = "secret key"

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
	""" GET: gets random gif from giphy and displays it along with the option to see another gif and to 
	save the gif to their evernote account"""
	if request.method == "GET": 
		#if we do have the access token proceed to show them a gif they can save to Evernote
		if "access_token" in session.keys():
			#get random gif from giphy api
			response=requests.get("http://api.giphy.com/v1/gifs/random?api_key="+giphy_api_key).json()
			if not response:
				return render_template("error.html", error_message="error with connection to giphy")

			#get random image url and id from giphy api response
			giphy_url=response['data']['image_url']
			giphy_id=response['data']['id']

			#get tags and pass them to the page because the giphy api only shows tags for random images
			giphy_tags=''
			try:
				response['data']['tags']
				for tag in response['data']['tags']:
					giphy_tags+=tag+', '
				giphy_tags=giphy_tags[:-2]
			except KeyError:
				pass

			#present the page with the GIF on it to the user with the GIF metadata (tags, id, url)
			return render_template("index.html", giphy_url=giphy_url, giphy_id=giphy_id, giphy_tags=giphy_tags) 
			session["access_token"]
		
		#if their Evernote access_token session varible is not set redirect them to Evernote to authoirze the applicaiton
		else:
			client = EvernoteClient(
				consumer_key=CONSUMER_KEY,
				consumer_secret=CONSUMER_SECRET,
				sandbox= sandbox
				)
			try:
				request_token = client.get_request_token("http://localhost:"+str(port)+"/auth")
				session['oauth_token'] = request_token['oauth_token'] 
				session['oauth_token_secret'] = request_token['oauth_token_secret']
				authorize_url = client.get_authorize_url(request_token)
			except KeyError:
				return render_template("error.html", error_message="Invalid API key and/or secret.  Please check the values of consumer_key and consumer_secret in the server.py file are valid and refresh to reset.")
			else:
				return redirect(authorize_url+"&suggestedNotebookName=Giphy") #suggest notebook name of giphy to use
		
	"""POST: shows confomation of evernote gif save and presents option 
	to return to main page or see the note in evernote"""
	if request.method == 'POST':
		if request.form['giphy_id']:
			#get giphy_id from post request that was to be saved
			giphy_id=request.form['giphy_id']
			giphy_tags=request.form['giphy_tags']
			response=requests.get("http://api.giphy.com/v1/gifs/"+giphy_id+"?api_key="+giphy_api_key).json()
			giphy_url=response['data']['images']['original']['url']

			#generate Evernote client
			client = EvernoteClient(token=session["access_token"], sandbox=sandbox)
			user_store = client.get_user_store()
			note_store = client.get_note_store()
			notebooks = note_store.listNotebooks()

			#makes a dictionary with the names for keys and the guids as values
			notebooks_dict=dict()
			for notebook in notebooks:
				notebooks_dict[notebook.name]=notebook.guid

			#if app notebook key use that notebok to save notes into
			if len(notebooks)==1 and notebooks[0].defaultNotebook==False: #assume app notebok key
				giphyNotebookGuid=notebooks[0].guid
			elif "Giphy" in notebooks_dict.keys(): #if notebook named Giphy exists use that notebook
				giphyNotebookGuid=notebooks_dict['Giphy']
			else: #make new notebook
				try:
					notebook=Types.Notebook()
					notebook.name="Giphy"
					notebook=note_store.createNotebook(notebook)
					giphyNotebookGuid=notebook.guid
				except Errors.EDAMUserException: #single app notebok key
					giphyNotebookGuid=notebooks[0].guid

			#create note title with user name + giphy id for unique identifier
			note_title=response['data']['username']+"-"+response['data']['id']

			#check to see if note exists already
			notebook_filter=NoteStoreTypes.NoteFilter()
			notebook_filter.guid=giphyNotebookGuid
			result_spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)
			try:
				noteList    = note_store.findNotesMetadata(session["access_token"], notebook_filter,0 , 40000, result_spec)
				for note in noteList.notes:
					if note.title==note_title:
						shardId=user_store.getUser(session["access_token"]).shardId
						shareKey=note_store.shareNote(session["access_token"], note.guid)
						evernote_url="%s/shard/%s/sh/%s/%s" % (EN_URL,shardId,note.guid,shareKey)
						return render_template("already_there.html", giphy_url=giphy_url, evernote_url=evernote_url)
			except Errors.EDAMUserException: #if the key doesn't have read permissions just move on
				pass
			
			
			#get image
			image= requests.get(giphy_url, stream=True).content
			md5 = hashlib.md5()
			md5.update(image)
			gif_hash = md5.digest()

			#Move the data into the Evernote Data datatype
			data = Types.Data()
			data.size = len(image)
			data.bodyHash = gif_hash
			data.body = image

			#Put the data in the Evernote Resource datatype and add the metadata
			resource = Types.Resource()
			resource.mime = 'image/gif'
			resource.data = data
			hash_hex = binascii.hexlify(gif_hash)
			
			#Create a new note
			note = Types.Note()
			note.notebookGuid=giphyNotebookGuid #create note for our Giphy notebook
			
			#Set Note title and contents
			note.title=note_title #name based on Giphy username and id
			note.content = '<?xml version="1.0" encoding="UTF-8"?>'
			note.content += '<!DOCTYPE en-note SYSTEM ' \
			    '"http://xml.evernote.com/pub/enml2.dtd">'
			note.content += '<en-note><br/>'
			note.content += '<en-media type="image/gif" hash="' + hash_hex + '"/>'
			note.content += '</en-note>'

			#add tags to the note
			enTagList=note_store.listTags()
			enTagListNames= [tag.name for tag in enTagList]
			giphyTagList=giphy_tags.split(", ")

			#If there are no tags make it an empty list
			if not note.tagGuids:
				note.tagGuids=[]

			#
			for giphyTag in giphyTagList:
				if giphyTag in enTagListNames:
					for tag in enTagList:
						if tag.name == giphyTag:
							note.tagGuids.append(tag.guid)
				elif giphyTag=='':
					continue
				else:
					tag=Types.Tag()
					tag.name=giphyTag
					tag=note_store.createTag(tag)

					note.tagGuids.append(tag.guid)


			note.resources = [resource] # Now, add the new Resource to the note's list of resources
			note=note_store.createNote(note) # create the note
			
			user=user_store.getUser(session["access_token"])
			shardId=user.shardId
			
			#Share the note to present it to the user in-browser
			try:
				shareKey=note_store.shareNote(session["access_token"], note.guid)
				evernote_url="%s/shard/%s/sh/%s/%s" % (EN_URL,shardId,note.guid,shareKey)
			except Errors.EDAMUserException:
				evernote_url=EN_URL + "/Home.action" #If the note cannot be shared redirect them to the Evernote web app
			return render_template("saved.html", giphy_url=giphy_url, evernote_url=evernote_url)
		else:
			#If the GIF displayed is no loger avalible present the user with an error
			return render_template("error.html", error_message="Error finding the GIF")

	else:
		return render_template("error.html", error_message="Unsuported HTTP method.  Please use GET or POST.")

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
