import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#The process of mapping URLs to functions is called "routing."
@app.route("/", methods = ["GET"])
def home():
	return "<h1>Distant Reading Archive</h1><p>Hello world</p>"

app.run()