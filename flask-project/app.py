from flask import Flask
from flask_cors import CORS, cross_origin

import service as service


app = Flask(__name__)
cors = CORS(app)

@app.route("/select/<id>")
@cross_origin()
def select(id):
    return service.select(id)