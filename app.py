######################################################################
# AUTHOR:     Andy Qin <andy.qin@datarobot.com>
# DATE:       2019-March-12
# DISCLAIMER: This application has only been tested in Python 3.6.4
######################################################################


from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import logging
from logging.config import dictConfig
from datetime import datetime
import datarobot as dr
import pandas as pd 
import requests



# A helper function that turns a datetime object into a string of desirable format
def formatDatetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# Configuring the logging format
dictConfig({
    "version": 1,
    "formatters": {"default": {
        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    }},
    "handlers": {"wsgi": {
        "class": 'logging.StreamHandler',
        "stream": "ext://flask.logging.wsgi_errors_stream",
        "formatter": "default"
    }},
    "root": {
        "level": "WARNING",
        "handlers": ["wsgi"]
    }
})


# This is a container that stores all customer complaints. Each complaint is a dict.
# We have prepopulated it with some complaints for demo purpose.
complaints = [{
    "narrative" : "My home has been under the short sale program for several months with SPS, we have presented several offers to this company and all have come back being denied, my property needs repairs, we have been working with a buyer for several weeks that has spent time and money to prepare a bid for repairs for this lender...",
    "name" : "Michael Scofield",
    "email" : "michael.scofield@gmail.com",
    "prediction" : "Mortgage",
    "time" : formatDatetime(datetime.now())
},{
    "narrative" : "I submitted a debit card dispute from my XXXX purchase in XXXX, XXXX. When I got home from XXXX, I read about all these XXXX scams in XXXX-where I purchased from their factory. I read articles that jade is enhanced for mass production and called XXXX and there is no way to tell if the jade is real or not. No one in my XXXX group bought any jade. Only I made a purchase at the jade factory in XXXX. I was concerned that I 'd been taken for granted by my tour...",
    "name" : "James Bond",
    "email" : "james.bond@gmail.com",
    "prediction" : "Bank account or service",
    "time" : formatDatetime(datetime.now())
},{
    "narrative" : "On XX/XX/2017, I've paid in full XXXX education loans. Details are below : 1. XXXX Amount of payment {$22000.00} 2. XXXX Amount of payment {$20000.00} Customer service representative, who provide me with a payoff amount, told me that both loans will be marked 'Paid in full' and I'll receive electronic 'PAID IN FULL NOTIFICATION' once my payments clear...",
    "name" : "Ethan Hunt",
    "email" : "ethan.hunt@gmail.com",
    "prediction" : "Student loan",
    "time" : formatDatetime(datetime.now())
}]


# Instantiate the app and the socket IO. Socket IO is used for server-client communication
app = Flask(__name__)
socketIo = SocketIO(app)


# Render complain.html when opening localhost:5000/
@app.route("/")
def complainPage():
    return render_template("complain.html")


# Render dashboard.html when opening localhost:5000/dashboard
@app.route("/dashboard")
def dashboardPage():
    return render_template("dashboard.html")


# Logging when a user log onto the complaint.html page
@socketIo.on("user-connect")
def userConnectionHandler(message):
    logging.warning("User connected")


# This function does two things:
#   1) Logging when an admin log onto the dashboard.html page
#   2) Emit existing complaints to this dashboard (only)
@socketIo.on("dashboard-connect")
def dashboardConnectionHandler(message):
    logging.warning("Dashboard connected")
    emit("complaint-with-prediction", complaints)


# This is the prediction making part. When a complaint is sent off by a customer, this function catches
# the complaint and predicts what product this complaint is related to. 
# The complaint & prediction is subsequently stored in 'complaints', and also broadcast to
# all connected dashboards.
@socketIo.on("complaint")
def complaintHandler(complaint, methods=["GET", "POST"]):
    print(complaint)
    #complaint["prediction"] = predict(complaint['narrative'])
    complaint["time"] = formatDatetime(datetime.now())
    logging.warning(str(complaint))
    complaints.append(complaint)
    emit("complaint-with-prediction", [complaint], broadcast=True)


# Start the app
if __name__ == "__main__":
    socketIo.run(app, debug=False)

    