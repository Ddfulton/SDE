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
import subprocess
from time import sleep
import pymysql

### Driver dependencies ###
import subprocess
import driver

### API dependencies ###
import newClient

### General configuration ###
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'application/json'


@app.route('/', methods=["GET", "POST", "OPTIONS"])
@cross_origin(origin="*")
def index():
    return render_template("index.html")

@app.route('/about', methods=["GET"])

def about():
    return render_template('about.html')


@app.route('/disclaimer', methods=["GET"])
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/unregister', methods = ["GET"])
@cross_origin(origin="*")
def unregister():
    return render_template("unregister.html")

@app.route('/registerCourse', methods=["POST", "OPTIONS"])
@cross_origin(origin="*")
def ajax():
    """
    This is where users sign up for the serice.
    """
    #TODO: Make sure class is in their shopping cart

    if request.method == "POST":
        goods = request.json

        if not driver.verify_onyen(goods["onyen"], goods["password"]):

            user_email = goods["onyen"] + "@live.unc.edu"
            print("ERROR: Onyen %s did not pass verification" % (goods["onyen"]))
            msg = "Dear %s,\n\nYour password did not match your onyen when we tried to verify it. Remember, in order for this to work:\n\n1. The course must be in your shopping cart.\n\n2. You must have room in your schedule.\n\n3. You must not have any other registration issues (for example, a hold).\n\nTry again!\n\nBest,\n\nSwap Drop Enroll" % (goods["onyen"])
            driver.send_email(user_email, "Incorrect Password", msg)
            failure_message = "%s did not pass verification. Terminating." % (goods["onyen"])

            return failure_message, 200



        print("INFO: REGISTERING %s IN THE DATABASE FOR %s" % (goods['onyen'], goods['course']))
        print("INFO: They were referred by %s" % goods['referringOnyen'])

        if goods['referringOnyen'] == "None":
            referringOnyen = None
        else:
            referringOnyen = goods['referringOnyen']

        registration = newClient.registerCourse(goods["onyen"], goods["password"], goods["course"], 1, 0, _referringOnyen=referringOnyen)

        if registration == False:
            user_email = goods["onyen"] + "@live.unc.edu"
            driver.send_email(user_email, "Already Registered", "Dear %s,\n\nYou were already registered for %s. You can't register more than once. Instead, refer your friends to put your name in the hat multiple times!\n\nRegards,\n\nSwap Drop Enroll" % (goods["onyen"], goods["course"]))
            return "User was already registered", 200

        driver.class_checker(goods['course'])


        msg = "Welcome to Swap Drop Enroll!\n\nAssuming that we have the correct credentials for your ConnectCarolina login, our program will automatically enroll you in %s when a spot opens up.\n\nTo make sure that the program will work for you, please check the following in ConnectCarolina:\n\n1.   Your desired class must be in your shopping cart. \n2.  You should not have any scheduling conflicts with the class.\n3.    You should not already be enrolled in a different section of the class.*\n\n *If you are trying to enroll in CHEM 101 at 12:00PM, but you are already enrolled in CHEM 101 at 8:00AM, then ConnectCarolina will block us from enrolling you. We will be adding this swap functionality for Spring 2017 registration.\n\nWhile you are ultimately responsible for disclosing your personal information with a third party, we would like to assure you that we use a secure encrypted database to protect your login information. At no point are we able to see your password, and your information is deleted forever when you unregister from our program.\n\nRegards,\n\nSwap Drop Enroll Team" % (goods["course"])

        user_email = goods["onyen"] + "@live.unc.edu"
        driver.send_email(user_email, "Welcome to Swap Drop Enroll", msg)
        driver.send_email('fulton.derek@gmail.com', 'INFO: New User', '%s has signed up for %s' % (goods['onyen'], goods['course']))
    else:
        pass

    return "Suh", 200


@app.route('/parse', methods=["POST"])
@cross_origin()
def parser():
    if request.method == "POST":

        try:
            envelope = simplejson.loads(request.form.get('envelope'))
        except:
            print("INFO: Failed to load envelope")

        status = "closed"


        try:
            from_address, to_address, subject, text, course, status = driver.parse_email(envelope)
        except:
            print("INFO: Failed to parse envelope")


        if status == "open":
            print("INFO: %s is Open" % course)

            nextUser = newClient.getNextUser(course)
            print("DEBUG: Just fetched %s" % nextUser)

            if nextUser != None:
                try:
                    subprocess.call(["ruby", "driver.rb", nextUser["onyen"], nextUser["password"], nextUser["course"]])

                    user_email = nextUser["onyen"] + "@live.unc.edu"
                    image_title = "%s_%s.png" % (nextUser["onyen"], nextUser["course"])

                    if driver.check_color(image_title) == True: # If green circle
                        newClient.markSuccess(nextUser["onyen"], nextUser["course"])
                        print("INFO: There was green circle. Marking success.")
                    else:
                        print("INFO: There was no green circle. Failure.")
                        pass

                    msg = "Dear %s,\n\nWe just attempted to enroll you in %s, but there appears to have been an error. Attached is a screenshot of the enrollment confirmation page.\n\nRegards,\nSwap Drop Enroll" % (nextUser["onyen"], nextUser["course"], attachment=image_title)
                    driver.send_email("fulton.derek@gmail.com", "INFO: Attempted enrollment", msg)
                    driver.send_email(user_email, "Your Swap Drop Enroll Result", "%s attempted to enroll in %s" % (nextUser["onyen"], nextUser["course"]), attachment=image_title)

                except:
                    print("DIDN'T WORK IN TRY")

            else:
                print("INFO: nextOnyen is None so we are untracking this course")

                driver.untrack(course)

                fail_message = "There was no nextOnyen for %s" % course

                return fail_message, 200

        elif status == "wait list":
            print("INFO: Wait list")

        elif status == "closed":
            print("INFO: Course is Closed")

        else:
            print("SPAM")

        return "Suh", 200

@app.route('/removeClass', methods = ['GET'])
@cross_origin()
def removeClass():
    return render_template("removeClass.html")


@app.route('/removeClassRequest', methods = ["GET", "POST"])
@cross_origin()
def removeClassRequest():
    if request.method == "POST":
        goods = request.json

        if newClient.unregister(goods["onyen"], goods["password"]):
            user_email = goods["onyen"] + "@live.unc.edu"
            driver.send_email(user_email, "Removed Class", "Dear %s,\n\nWe have removed %s from our database. We hope you had a positive experience.\n\nIf you ever have any questions or concerns, feel free to shoot us an e-mail at blowjangles@protonmail.com.\n\nRegards,\n\nSwap Drop Enroll" % (goods["onyen"], goods["course"]))
            return "Success", 200
        else:
            user_email = goods["onyen"] + "@live.unc.edu"
            driver.send_email(user_email, "Incorrect password", "Dear %s,\n\nWe tried to unregister %s you from our database, but your passwords didn't match. If you believe this is a mistake, please don't hesitate to e-mail us at blowjangles@protonmail.com so that we can manually unregister you.\n\nRegards,\n\nSwap Drop Enroll" % (goods["onyen"], goods["course"]))
            return "Success", 200

        return "Success", 200
    return "Success", 200





@app.route('/unregisterRequest', methods = ["GET", "POST"])
@cross_origin()
def unregisterRequest():
    if request.method == "POST":
        goods = request.json


        result = newClient.unregister(goods["onyen"], goods["password"])

        if result == True:
            user_email = goods["onyen"] + "@live.unc.edu"
            driver.send_email(user_email, "Goodbye from Swap Drop Enroll", "Dear %s,\n\nWe have removed you completely from our database. We hope you had a positive experience.\n\nIf you ever have any questions or concerns, feel free to shoot us an e-mail at blowjangles@protonmail.com.\n\nRegards,\n\nSwap Drop Enroll" % (goods["onyen"]))

            return "Success", 200
        elif result == "NO USER":
            user_email = goods["onyen"] + "@live.unc.edu"
            driver.send_email(user_email, "User does not exist","Hello,\n\nYou tried to unregister from Swap Drop Enroll but we didn't find you in the database. So you're already out. If you miss us, feel free to sign up again.\n\nRegards,\n\nSwap Drop Enroll")

            return "Suh dood", 200
        else:
            print("Passwords didn't match")
            user_email = goods["onyen"] + "@live.unc.edu"
            driver.send_email(user_email, "Incorrect password", "Dear %s,\n\nWe tried to unregister you from our database, but your passwords didn't match. If you believe this is a mistake, please don't hesitate to e-mail us at blowjangles@protonmail.com so that we can manually unregister you.\n\nRegards,\n\nSwap Drop Enroll" % (goods["onyen"]))

            return "Suh dood", 200

        return "Suh dood", 200

    return "Suh dood", 200




if __name__ == '__main__':
    app.run(debug=True)
