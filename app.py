# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
import json
import subprocess
import driver
import simplejson
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/parse', methods=["POST"])
def parser():
    # Required response to SendGrid.com’s Parse API
    print("HTTP/1.1 200 OK")

    # Consume the entire email
    envelope = simplejson.loads(request.form.get('envelope'))

    from_address, to_address, subject, body = driver.parse_email(envelope)

    right_now = datetime.now()

    body = """
	From: %s\n
	To: %s\n
	Subject: %s\n
	Body: %s\n
	""" % (from_address, to_address, subject, body)

	# DRIVE AND GET RESULTS HERE
    print("E-mailing the body:\n%s"%body)
    driver.send_email("fulton.derek@gmail.com", "DEBUGGING SDE at %s" % right_now, body)


if __name__ == '__main__':
    app.run(debug=True)

