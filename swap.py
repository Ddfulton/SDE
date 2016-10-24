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
 * Author: We'll never tell
 * Version: 20160818
 * TODO: Add swap functionality and professionalize the frontend for Spring 2017
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
import newClient

### General configuration ###
app = Flask(__name__)  
CORS(app)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/feedback', methods=["POST", "OPTIONS"])
@cross_origin()
def feedback():
    if request.method == "POST":
        print("INFO: Someone submitted feedback")

        driver.send_email('fulton.derek@gmail.com', "Swap Drop Enroll Feedback", request.json["feedback"])

@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')


@app.route('/disclaimer', methods=["GET"])
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/ajax', methods=["POST", "OPTIONS"])
@cross_origin()
def ajax():
    """
    This is where users sign up for the serice. 
    """
    #TODO: Make sure class is in their shopping cart

    if request.method == "POST":
        print("INFO: /ajax WAS POSTED")
        goods = request.json

        # if not driver.verify_onyen(goods["onyen"], goods["password"]):
            
        #     print("ERROR: Onyen %s did not pass verification" % (goods["onyen"]))
        #     driver.send_email(goods["email"], "Incorrect Password", "Your password did not match your onyen (%s). Therefore, we didn't sign you up for shit. So try again with the right password!" % goods["onyen"])
        #     failure_message = "%s did not pass verification. Terminating." % (goods["onyen"])
            
        #     return failure_message, 200


        print("INFO: REGISTERING %s IN THE DATABASE FOR %s" % (goods['onyen'], goods['course']))

        registration = newClient.registerCourse(goods["onyen"], goods["password"], goods["course"], 1, 0, goods["mobile"], _referringOnyen=goods["referringOnyen"])
        
        if registration == False:
            return "User was already registered", 200

        # driver.class_checker(goods['course'])

        msg = """Dear %s,\n

        Welcome to Swap Drop Enroll. The way this works is it waits for an e-mail
        from classchecker, and then if it sees "%s has changed from closed to open" it instantly fetches
        your credentials (securely) and registers you.

        You *must* not have any schedule conflicts with the class and it *must* be 
        in your shopping cart. 

        We will be adding swap functionality for Spring 2017 registration. 

        We use a token, a cipher, and encryption to protect your password. So, while 
        you are ultimately responsible for your own password, and agree to take responsibility
        for that when you sign up, we never see your actual password. 

        Regards,

        Swap Drop Enroll

        
        """ % (goods['onyen'], goods['course'])

        driver.send_email(goods['email'], 'Swap Drop Enroll', msg)
        driver.send_email('fulton.derek@gmail.com', 'NEW USER',
                          '%s has signed up for %s' % (goods['onyen'], goods['course']))
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

        nextUser = newClient.getNextUser(course)

        if nextUser != None:

            try:

                driver.enroll(nextUser["onyen"], nextUser["password"], nextUser["course"]) #TODO: Result = driver.enroll and then send the proper e-mail

                print("INFO: Sending e-mail to fulton.derek@gmail.com and %s" % onyenInfo.email)
                image_title = "%s_%s.png" % (nextOnyen, course)

                driver.send_email('fulton.derek@gmail.com', 'Your Swap Drop Enroll Result',
                                  'just tried to enroll %s in %s.\nIf you would like to stop tracking this course, visit https://www.swapdropenroll.com/removeClass.' % (nextOnyen, course), attachment=image_title)

                driver.send_email(onyenInfo.email, 'Your Swap Drop Enroll Result',
                                  'Just tried to enroll %s in %s.\nIf you would like to stop tracking this course, visit https://www.swapdropenroll.com/removeClass.' % (nextOnyen, course), attachment=image_title)
                
            except:
                print("Did not make it through the try to enroll block of code. This could be because the class is not in the shopping cart.")



        elif nextUser == None:
            print("INFO: nextOnyen is None so we are untracking this course")

            driver.untrack(course)

            fail_message = "There was no nextOnyen for %s" % course

    elif status == "wait list":
        print("INFO: Wait list")

    elif status == "closed":
        print("INFO: Course is Closed")

    else:
        print("SPAM")

    return "Suh", 200

@app.route('/removeClass', methods = ['GET'])
def removeClass():
    return render_template("removeClass.html")

@app.route('/removeClassReq', methods = ['POST'])
def processClassRemoval():
    if request.method == "POST":
        print("INFO: /removeClassReq WAS POSTED")
        goods = request.json
        
        onyenInfo = SDEClient.getOnyenInfo(goods['onyen'])

        if onyenInfo.onyen == "0":
            print("INFO: No record found for specified onyen %s, ignoring request" % goods['onyen'])

            return "Suh", 200
        
        print("INFO: Removing class %s for Onyen %s" % (goods['course'], goods['onyen']))

        try: 
            print(SDEClient.markEnrollPass(goods['onyen'], goods['course']))
            
            try:
                driver.send_email(onyenInfo.email, "Unregister", "We just removed %s from %s" % (goods["onyen"], goods["course"]))
            
            except:
                print("driver.send_email broke on processClassRemoval()")
        
        except:
            print("ERROR: Something happened")

        return "Request successful", 200

    else:
        return "Suh", 200

@app.route('/unregister', methods = ['GET'])
def unregister():
    return render_template("unregister.html")

@app.route('/unregisterReq', methods = ['POST'])
def proccessUnregister():
    if request.method == "POST":
        print("INFO: /unregisterReq WAS POSTED")
        goods = request.json

        onyenInfo = SDEClient.getOnyenInfo(goods['onyen'])

        if onyenInfo.onyen == "0":
            print("INFO: No record found for specified onyen %s, ignoring request" % goods['onyen'])

            return "Suh", 200

        try: 
            print(SDEClient.deleteUser(goods['onyen'], goods['password']))
            
            try:
                driver.send_email(onyenInfo.email, "Goodbye", "We just removed %s completely. Goodbye." % goods["onyen"])
            except:
                print("driver.send_email broke on processUnregister()")

        except:
            print("ERROR: Something happened")

        return "Request successful", 200

    else:
        return "Suh", 200


if __name__ == '__main__':
    app.run(debug=True)
