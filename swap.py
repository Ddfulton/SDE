# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, make_response
import json
import subprocess
import driver
import simplejson
from datetime import datetime
from werkzeug.local import Local
import SDEClient
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')


@app.route('/disclaimer', methods=["GET"])
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/ajax', methods=["GET", "POST", "OPTIONS"])
@cross_origin()
def ajax():
    if request.method == "POST":
        print("INFO: /ajax WAS POSTED")
        goods = request.json

        print("REGISTERING %s IN THE DATABASE FOR %s WITH ZEEP" % (goods['onyen'], goods['course']))

        print(SDEClient.registerOnyen(goods['onyen'], goods['password'], goods['email']))
        print(SDEClient.registerClass(goods['onyen'], goods['course']))

        print("SIGNING UP TO TRACK %s" % goods['course'])
        driver.class_checker(goods['course'])

        msg = """Dear %s,\n

		You just signed up for %s.

		Welcome to Swap Drop Enroll. This service waits for an e-mail from classchecker, reads that email, 
		and if the status changes from Closed to Open, it fetches your password and enrolls you. 

		We use three layers of security to protect your password. If you are interested, 
		we use a SOAP client with both a token and cipher, among other security features. 

		Feel free to contact us at swapdropenroll@gmail.com.

		Warm regards, 

		Swap Drop Enroll
		""" % (goods['onyen'], goods['course'])

        driver.send_email(goods['email'], 'Swap Drop Enroll', msg)
    else:
        pass

    return "Suh", 200


@app.route('/parse', methods=["GET", "POST"])
@cross_origin()
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
            # TODO Also get next e-mail
            onyenPassword = SDEClient.getLoginInfo(nextOnyen)

            print("INFO: Enrolling %s in %s" % (nextOnyen, course))
            
            try:

                driver.enroll(nextOnyen, onyenPassword, course)
                
                print("INFO: Sending e-mail to fulton.derek@gmail.com and %s@live.unc.edu" % nextOnyen)
                image_title = "%s_%s.png" % (nextOnyen, course)
                driver.send_email('fulton.derek@gmail.com', 'Your Swap Drop Enroll Result',
	                              'just tried to enroll %s in %s.' % (nextOnyen, course), attachment=image_title)

                user_email = nextOnyen + "@live.unc.edu"

                driver.send_email(user_email, 'Your Swap Drop Enroll Result',
	                              'Just tried to enroll %s in %s' % (nextOnyen, course), attachment=image_title)


            except:
                print("Did not make it through the try to enroll block of code.")
            

        else:
            print("INFO: nextOnyen is NONE")
            fail_message = "There was no nextOnyen for %s" % course
            



    elif status == "wait list":
        print("Wait")



    elif status == "closed":
        print("INFO: ")

    else:
        print("SPAM")

    return "Suh", 200


if __name__ == '__main__':
    app.run()
