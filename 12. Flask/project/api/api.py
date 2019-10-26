import flask
from flask import request, jsonify

# creating flask object
app = flask.Flask(__name__)

# to get error if exist
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
# list contains 3 dictionaries with keys,id,title,author,first_sentence,year_published
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

#The process of mapping URLs to functions is called "routing."
@app.route("/", methods = ["GET"])
def home():
	return "<h1>Distant Reading Archive</h1><p>Hello world</p>"

# Creating a route which return all of the available entries in our catalog.
@app.route("/api/books/all", methods = ["GET"])
def api_all():
	return jsonify(books)


# filtering capabilities
@app.route("/api/books", methods = ["GET"])
def api_id():
	# Check if an id was provided as part of the URL
	# if ID is provided, assign it to a variable
	# if ID is not provided,display an error in the browser
	if 'id' in request.args:
		id = int(request.args['id'])
	else:
		return "Error: No id field provided. Please specify an id."

	# Create an empty list for our results
	results = []

	# Loop through the data and match results that fit the requested ID.
	# IDs are unique, but other fields might return many results
	for book in books:
		if book['id'] == id:
			results.append(book)


	# Use the jsonify function from Flask to convert our list of 
	# Python dictionaries to the JSON format.
	return jsonify(results)
	# run code using localhost:5000/api/books?id=0
	# ? this is query parameter
app.run()