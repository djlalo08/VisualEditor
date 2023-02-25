from flask import Flask, session
from flask_cors import CORS, cross_origin
from flask_session import Session

import load_ir_from_text as lift
from ir_utils import index

import service as service
from clojure_to_jsx.Jsxify import to_jsx

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY']= 'keyyyy'
sess = Session()

@app.route("/select/<id>")
@cross_origin()
def select(id):
    print("selecting:", id)
    if not session['inited']:
        print("ir not inited. Initing...")
        init()
        session['inited'] = True
    else:
        print("Session has already been inited")

    service.select(id, session['ir'], session['id_map'])
    return '0'


@app.route("/clear")
def clear():
    session['inited'] = None
    session['ir'] = None
    session['id_map'] = {}
    return str(session)

@app.route("/show/<item>")
@cross_origin()
def show(item):
    if item == 'all': return str(session)
    if item in session:
        return str(session[item])

    return 'Item not found'

def init():
    print("initializing")
    ir_file = open('./ir', 'r')
    lines = ir_file.read()

    session['ir'] = lift.parse(lines)
    session['id_map'] = index(session['ir'])


def reset():
    print("initializing")
    ir_file = open('./ir', 'r')
    lines = ir_file.read()

    ir = lift.parse(lines)
    jsx = to_jsx(ir)

    file = open('../webapp/displayer/src/Components/GeneratedApp.js', 'w')
    file.write(jsx)
    file.close()


if __name__ == "__main__":
    # reset()
    sess.init_app(app)

    app.debug = True
    app.run()