"""
/*  (    (           
 *  )\ ) )\ )        
 *  (()/((()/(   (    
 *  /(_))/(_))  )\   
 *  (_)) (_))_  ((_)  
 *  / __| |   \ | __| 
 *  \__ \ | |) || _|  
 *  |___/ |___/ |___| 
 *
 * Project: Swap Drop Enroll
 * Author: SDE Team (Derek Fulton and Sam Andersen)
 * Version: 20160816
 * TODO: Continue adding functionality
 *
 */
"""
# -*- encoding: utf-8 -*-

### Flask dependencies ###
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_cors import CORS, cross_origin
import json
import simplejson
from datetime import datetime
from werkzeug.local import Local

### Driver dependencies ###
import subprocess
import driver

### API dependencies ###
import SDEClient

### General configuration ###
app = Flask(__name__) # Define the Flask application
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

@app.route('/ajax', methods=["POST", "OPTIONS"])
@cross_origin()
def ajax():
	### TODO Make sure their password is correct and it's in their shopping cart ### 
    if request.method == "POST":
        print("INFO: /ajax WAS POSTED")
        goods = request.json

        print("REGISTERING %s IN THE DATABASE FOR %s WITH ZEEP" % (goods['onyen'], goods['course']))

        print(SDEClient.registerOnyen(goods['onyen'], goods['password'], goods['email'])) # API connection
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

@app.route('/test', methods=["GET", "POST"])
def test():
    if request.method == "POST":
        print("Got POST")
    else:
        pass

    return "Suh", 200

@app.route('/parse', methods=["POST"])
@cross_origin()
def parser():
    
    if request.method == "POST":
        print("Request is a POST")
	    
    try:
        envelope = simplejson.loads(request.form.get('envelope'))
        print(envelope)

    except:
        print("INFO: Failed to load envelope")

    status = "closed"
    try:
        from_address, to_address, subject, text, course, status = driver.parse_email(envelope)

    except:
        print("INFO: Failed to parse envelope")
        course = "INFO: Failed to parse envelope"

    if status == "open":
        print("INFO: %s is Open" % course)

        nextOnyen = SDEClient.getNextUser(course)

        if nextOnyen != "NONE" and nextOnyen not None:
            # TODO Also get next e-mail
            onyenPassword = SDEClient.getLoginInfo(nextOnyen)
	            
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
            # TODO remove the course from the database if it's none
            fail_message = "There was no nextOnyen for %s" % course
	            



    elif status == "wait list":
        print("INFO: Wait list")

    elif status == "closed":
        print("INFO: Course is Closed")

    else:
        print("SPAM")

    return "Suh", 200


if __name__ == '__main__':
    app.run()
