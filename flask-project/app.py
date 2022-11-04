from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route("/select/<id>")
@cross_origin()
def hello_world(id):
    return f"selected id is {id}"
