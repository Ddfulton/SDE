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

@app.route('/about', methods=["GET"])
def about():
	return render_template('about.html')

@app.route('/disclaimer', methods=["GET"])
def disclaimer():
	return render_template('disclaimer.html')

@app.route('/ajax', methods=["GET", "POST"])
def ajax():
	if request.method == "POST":
		goods = request.json

		print("REGISTERING %s IN THE DATABASE FOR %s WITH ZEEP" % (goods['onyen'], goods['course']))
		
		print(SDEClient.registerOnyen(goods['onyen'], goods['password'], goods['email']))
		print(SDEClient.registerClass(goods['onyen'], goods['course']))

		msg = """
		Dear %s, 

		Welcome to Swap Drop Enroll. This service waits for an e-mail from classchecker, reads that email, 
		and if the status changes from Closed to Open, it fetches your password and enrolls you. 

		We use three layers of security to protect your password. If you are interested, 
		we use a SOAP client with both a token and cipher, among other security features. 

		Feel free to contact us at swapdropenroll@gmail.com.

		Warm regards, 

		Swap Drop Enroll
		"""

		driver.send_email(goods['email'], 'Swap Drop Enroll', msg)
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

			print("INFO: Enrolling %s in %s" % (nextOnyen, course))
			driver.enroll(nextOnyen, onyenPassword, course)

			
			print("INFO: Sending e-mail to fulton.derek@gmail.com")
			image_title = "%s_%s.png"%(nextOnyen, course)
			driver.send_email('fulton.derek@gmail.com', 'Your Swap Drop Enroll Result', 'just tried to enroll %s in %s'%(nextOnyen, course), attachment=image_title)

			#TODO
			# if enrollment successful
			# zeep.removeOnyen

			return "Success", 200
	if status == "wait list":
		print("Wait")

		return "Success", 200

	if status == "closed":
		return "Success", 200

	else:
		print("SPAM")
		return "Success", 200
		


	return "Success", 200

if __name__ == '__main__':
    app.run()