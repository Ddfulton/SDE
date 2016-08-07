# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response
import json
import subprocess
import driver
import simplejson
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")

def contact():
    return render_template("contact.html")


@app.route('/parse', methods=["POST"])
def parser():
    """
    Process POST request from Sendgrid Inbound Parse. Assign variables from_address, to_address, subject and body.
    If body contains "closed to open", query the database and run driver.drive (register user on ConnectCarolina)
    """

    # Required response to SendGrid.com’s Parse API
    print("HTTP/1.1 200 OK")

    envelope = simplejson.loads(request.form.get('envelope'))
    from_address, to_address, subject, body, course, status = driver.parse_email(envelope)

    if status == "open":
        # onyen = query database
        # password = query database
        # driver.enroll(onyen, password, course)
        # user_email
        # driver.send_email(user_email, "Swap Drop Enroll", body, image)
        pass

    elif status == "closed":
        pass
        # Status is closed

    else: # Probably not sendgrid
        pass

    response = Response(status=200)

    return response


if __name__ == '__main__':
    app.run(debug=True)

