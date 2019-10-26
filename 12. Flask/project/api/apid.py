# Connecting Our API to a database
# Implementing error handling

import flask
import sqlite3
from flask import request, jsonify

# creating flask object
app = flask.Flask(__name__)

# to get error if exist
app.config["DEBUG"] = True

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

#The process of mapping URLs to functions is called "routing."
@app.route("/", methods = ["GET"])
def home():
	return "<h1>Distant Reading Archive</h1><p>Hello world</p>"

# Creating a route which return all of the available entries in our catalog.
@app.route("/api/books/all", methods = ["GET"])
def api_all():
	conn = sqlite3.connect('books.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	all_books = cur.execute("SELECT * FROM books;").fetchall()

	return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(e):
	return "<h1>404</h1><p>The resource could not be found.</p>"

# filtering capabilities
@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)
	# run code using localhost:5000/api/books?id=0
	# ? this is query parameter
app.run()