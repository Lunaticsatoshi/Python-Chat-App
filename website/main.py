from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from client import Client
from threading import Thread
import time

NAME_KEY = "name"
client = None
messages = []
app = Flask(__name__)
app.secret_key = "hellouserwelcometotheworldofanime"

def disconnect():
    """
    Call before client disconnects
    """
    global client
    if client:
        client.disconnect()


@app.route("/login", methods = ["POST", "GET"])
def login():
    """
    display main login page and handles user name in session
    exception POST
    return none
    """
    disconnect()
    if request.method == "POST":
        print(request.form)
        session[NAME_KEY] = request.form["inputName"]
        return redirect(url_for("home"))
         
    return render_template("login.html", **{"session": "session"}) 

@app.route("/logout")
def logout():
    """
    Logs out user and pops user from session
    retuen none 
    """
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))

@app.route("/")
@app.route("/home")
def home():
    """
    Displays home page on Login
    return none
    """
    global client

    if NAME_KEY not in session:
        return redirect(url_for("login"))

    client = Client(session[NAME_KEY])
    return render_template("index.html", **{"login": True, "session": session})


@app.route("/send_messages", methods = ["GET"])
def send_message(url=None):
    """
    called from javascript function to send messages
    param: url
    return none
    """
    global client
    msg = request.args.get("val")
    print(msg)
    if client:
        client.send_message(msg)

    return "none"

@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})

def update_messages():
    """
     Updates the local list of messages
    """
    global messages
    run = True
    while run:
        time.sleep(0.1)#Updates every 0.1 seconds
        if not client:
            continue
        new_messages = client.get_messages() #Get new messages
        messages.extend(new_messages)

        for msg in new_messages:#Display messages
            print(msg)
            if msg == "{quit}":
                run = False
                break


if __name__ == "__main__":
    Thread(target= update_messages).start()
    app.run(debug= True)
    