# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, make_response
import json
import subprocess
import driver
import simplejson
from datetime import datetime
from werkzeug.local import Local
import SDEClient

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/ajax', methods=["GET", "POST"])
def ajax():
	if request.method == "POST":
		goods = request.json

		print("REGISTERING %s IN THE DATABASE FOR %s WITH ZEEP" % (goods['onyen'], goods['course']))
		
		print(SDEClient.registerOnyen(goods['onyen'], goods['password'], goods['email']))
		print(SDEClient.registerClass(goods['onyen'], goods['course']))

	else:
		return "Suh", 200


	return "Suh", 200


@app.route('/parse', methods=["GET", "POST"])
def parser():
	# Consume the entire email
	envelope = simplejson.loads(request.form.get('envelope'))
	print(envelope)

	from_address, to_address, subject, text, course, status = driver.parse_email(envelope)




			

	if status == "open":
		# Fetch credentials for course 
		# Enroll
		# Email result
		# Take user out of database if success
		print("INFO: %s is Open" % course)

		nextOnyen = SDEClient.getNextUser(course)

		if nextOnyen != "NONE":

			onyenPassword = SDEClient.getLoginInfo(nextOnyen)

			driver.enroll(nextOnyen, onyenPassword)


			image_title = "%s" %(nextOnyen) + "_%s" %(course)".png"
			driver.send_email('fulton.derek@gmail.com', 'TEST', 'just tried to enroll %s in %s'%(nextOnyen, course), attachment=)

			"""
			if success:
				print SDE.markEnrollPass(nextOnyen, course)
				send e-mail detailing results
			"""

	if status == "wait list":
		print("Wait")

	if status == "closed":
		pass

	else:
		print("SPAM")
		


	return "Success", 200

if __name__ == '__main__':
    app.run()