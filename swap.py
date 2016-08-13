# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, make_response
import json
import subprocess
import driver
import simplejson
from datetime import datetime
from werkzeug.local import Local


app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])

def index():
    return render_template("index.html")


@app.route('/ajax', methods=["POST"])
def ajax():
	if request.method == "POST":
		goods = request.json

		print("REGISTERING %s IN THE DATABASE FOR %s WITH ZEEP" % (goods['onyen'], goods['course']))
		
		### ZEEP ADD USER RIGHT HERE ###

	else:
		return "Suh", 200


	return "Suh", 200


@app.route('/parse', methods=["POST"])
def parser():
	# Required response to SendGrid.com’s Parse API
	print("GOT THE SENDGRID")

	# Consume the entire email
	envelope = simplejson.loads(request.form.get('envelope'))
	print(envelope)

	from_address, to_address, subject, text, course, status = driver.parse_email(envelope)




			###   TODO   ###

	if status == "open":
		# Fetch credentials for course 
		# Enroll
		# Email result
		# Take user out of database if success

	if status == "wait list":
		###TODO PSEUDO-CODE###
		# Wait list enroll
		# Same as status == "open"
	if status == "closed":
		pass
	else:
		# Catch for non-classchecker emails 
	
			###   END TODO   ###


	return "Success", 200

if __name__ == '__main__':
    app.run(debug=True)