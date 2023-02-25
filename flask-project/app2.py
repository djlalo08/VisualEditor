from flask import Flask, session
from flask_cors import CORS, cross_origin
from flask_session import Session

app = Flask(__name__)
cors = CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'keyyyy'
sess = Session()


@app.route("/go")
def go():
    if 'count' not in session:
        session['count'] = 0
    else:
        temp = session['count']
        session['count'] = temp + 1
    return str(session['count']) + '!'

@app.route("/reset")
def reset():
    session['count'] = 0
    return ''


if __name__ == "__main__":
    # reset()
    sess.init_app(app)

    app.debug = True
    app.run()