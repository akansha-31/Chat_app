from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, send
from models import Message
import os

app = Flask(__name__)
socketio = SocketIO(app)
db = SQLAlchemy(app, session_options={"autoflush": False})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.urandom(128)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://akansha:password@localhost:5432/chat_app'
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 86400
app.config["SQLALCHEMY_POOL_SIZE"] = 200
app.config["SQLALCHEMY_POOL_RECYCLE"] = 100
app.config["ENV"] = "development"


@app.route("/chat_room")
def chat_room():
    print("Session: ", session)
    if "logged" in session and "username" in session:
        messages = Message.query.all()
        return render_template("chat_room.html", messages=messages)
    else:
        return redirect(url_for("register"))


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session["logged"] = True
        session["username"] = request.form.get("username")
        return redirect(url_for("chat_room"))
    if request.method == "GET":
        if "logged" in session and "username" in session:
            return redirect(url_for("chat_room"))
        else:
            return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("register"))


def save_message(sender, message, date):
    """
    function to save message into database
    """
    add_message = Message(username=sender, message=message, date=date)
    db.session.add(add_message)
    db.session.commit()


@socketio.on('message')
def handleMessage(msg):
    import json

    response = json.loads(msg)
    print(msg)
    save_message(response["sender"], response["msg"], response["date"])
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)
