# Import the Evernote client
from evernote.api.client import EvernoteClient

# Import the Evernote note storetypes to get note datatypes 
# to properly get note/tag counts (note filter)
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.type.ttypes as Types

# Define access token either:
# Developer Tokens (https://dev.evernote.com/doc/articles/dev_tokens.php)
# or OAuth (https://dev.evernote.com/doc/articles/authentication.php)
access_token = "insert dev or oauth token here"

# Setup the client
client = EvernoteClient(token = access_token, sandbox = True)

# Get note store object
note_store = client.get_note_store()

# Create note filter object
related_query = NoteStoreTypes.RelatedQuery()

# You must specify a note GUID or plainText (but not both!)
related_query.plainText = "Link your NYT Cooking and Evernote accounts to give all your recipes a single home. We enhanced the NYT Cooking Recipe Box. Along with the ability to save any of the 17 recipes from NYT Cooking you can now save recipes you find on other websites and in cookbooks  and even ones you written yourself. Save recipes from across the web with Evernote. Download the Evernote Web Clipper to save recipes into your NYT Cooking Recipe Box no matter where you find them. Once you link your Evernote and NYT Cooking accounts you have your recipes all in one place. Go from paper to screen  or create recipes from scratch. Use Evernote to take photos of your grandmother recipe cards or dishes you find in cookbooks. You can even write your own recipes directly in Evernote. All will now be available in your NYT Cooking Recipe Box. Access all of your recipes in one place across all of your devices. Whether you at home the grocery store or anywhere in between open NYT Cooking or Evernote to see all of your recipes. Get Started&oq=Link your NYT Cooking and Evernote accounts to give all your recipes a single home.  We enhanced the NYT Cooking Recipe Box. Along with the ability to save any of the 17 recipes from NYT Cooking you can now save recipes you find on other websites and in cookbooks  and even ones you written yourself. Save recipes from across the web with Evernote. Download the Evernote Web Clipper to save recipes into your NYT Cooking Recipe Box no matter where you find them. Once you link your Evernote and NYT Cooking accounts you have your recipes all in one place. Go from paper to screen  or create recipes from scratch. Use Evernote to take photos of your grandmother recipe cards or dishes you find in cookbooks. You can even write your own recipes directly in Evernote. All will now be available in your NYT Cooking Recipe Box. Access all of your recipes in one place across all of your devices. Whether you at home the grocery store or anywhere in between open NYT Cooking or Evernote to see all of your recipes. Get Started"

# Uncomment the following line to set the note GUID of the note you wish to get related results for
#YOU MUST COMMENT THE LINE ABOVE DEFINING THE 'plainText' ATTRIBUTE FOR RESULTS BASED ON A NOTE
#related_query.noteGuid = "insert note GUID to user for related results query here"

# [OPTIONAL] Create note filter object
note_filter = NoteStoreTypes.NoteFilter()
# Set note filter search grammer to get notes created in the last 2 days
note_filter.words = "updated:month-2"
# Uncommend the following line to set note filter tag GUIDs
#note_filter.tagGuids = ["GUID of tag1", "GUID of tag 2", "...."]
# Set note filter order to descending
#note_filter.ascending =  False
# Set note filter inative attribute to False (will search only active notes)
# setting this value to True will only return search results that are in the trash
#note_filter.inactive = False
# Uncomment the following line to set note time zone of the search to 'America/Los_Angeles'
#note_filter.timeZone = "America/Los_Angeles"
# Uncomment the following line to set note filter emphasized attribute to additional 
# 'wish list' search grammer to be used in conjunction with the orinigal search query to 
# highlight search results 
#note_filter.emphasized = "any: tag:cool -tag:uncool"
# Uncomment the following line to set note filter includeAllReadableNotebooks attribute
# to include all readable business notebooks in a search
# search must be performed on a business note store with a business auth token
#note_filter.includeAllReadableNotebooks=True
# Attach note filter to related query object
related_query.filter = note_filter

# [OPTIONAL] set reference uri around which "relatedness" should be based
related_query.referenceUri = 'evernote.com'

# Create a result spec object for the findNotesMetadata method
result_spec = NoteStoreTypes.RelatedResultSpec()
# Set various result spec parameters (optional)
result_spec.maxNotes = 10
result_spec.maxNotebooks = 10  
result_spec.maxTags = 10
result_spec.writableNotebooksOnly = False
result_spec.includeContainingNotebooks = False
result_spec.maxRelatedContent = 100
# Set a list of types of related content to return
rel_content = Types.RelatedContentType()
result_spec.relatedContentTypes = [rel_content.NEWS_ARTICLE, rel_content.PROFILE_PERSON, rel_content.PROFILE_ORGANIZATION, rel_content.REFERENCE_MATERIAL]
# [OPTIONAL] Business attributes (only call on a business note)
# Uncommend the following lines to get users in the business as
# Related results
#result_spec.maxExperts = 5 #set max users to return



search_result = note_store.findRelated( related_query, result_spec)

if search_result.notes:
	print "Found %s related notes." % len(search_result.notes)
	if len(search_result.notes) >= 3:
		print "Here are the titles of 3 related notes:\n  * '%s'\n  * '%s'\n  * '%s'\n" % (search_result.notes[0].title, search_result.notes[1].title, search_result.notes[2].title)
if search_result.notebooks:
	print "Found %s related notebooks." % len(search_result.notebooks)
if search_result.tags:
	print "Found %s related tags." % len(search_result.tags)
if not search_result.notes and not search_result.notebooks and not search_result.tags:
	print "No related content found.  Try adding more content or another note GUID."
