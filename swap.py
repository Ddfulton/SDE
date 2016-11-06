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
            driver.send_email(user_email, "Incorrect Password", "Your password did not match your onyen (%s). Therefore, we didn't sign you up. So try again with the right password!" % goods["onyen"])
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
            return "User was already registered", 200

        driver.class_checker(goods['course'])


        msg = "Welcome to Swap Drop Enroll!\n\nAssuming that we have the correct credentials for your ConnectCarolina login, our program will automatically enroll you in %s when a spot opens up.\n\nTo make sure that the program will work for you, please check the following in ConnectCarolina:\n\n1.   Your desired class must be in your shopping cart. \n2.  You should not have any scheduling conflicts with the class.\n3.    You should not already be enrolled in a different section of the class.*\n\n *If you are trying to enroll in CHEM 101 at 12:00PM, but you are already enrolled in CHEM 101 at 8:00AM, then ConnectCarolina will block us from enrolling you. We will be adding this swap functionality for Spring 2017 registration.\n\nWhile you are ultimately responsible for disclosing your personal information with a third party, we would like to assure you that we use a secure encrypted database to protect your login information. At no point are we able to see your password, and your information is deleted forever when you unregister from our program.\n\nRegards,\n\nSwap Drop Enroll Team" % (nextUser["course"])

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

                    msg = "Dear %s,\n\nWe just attempted to enroll you in %s, but there appears to have been an error. Attached is a screenshot of the enrollment confirmation page.\n\nRegards,\nSwap Drop Enroll" % (nextUser["onyen"], nextUser["course"])
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

@app.route('/removeClassRequest', methods = ['POST'])
@cross_origin()
def processClassRemoval():
    if request.method == "POST":
        goods = request.json
        
        newClient.markSuccess()
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
@cross_origin()
def unregister():
    return render_template("unregister.html")

@app.route('/unregisterRequest', methods = ['POST'])
@cross_origin()
def proccessUnregister():
    if request.method == "POST":
        goods = request.json

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







import pymysql.cursors
import random


chickfila = "Tq8eGl70L0MFTSB0ywWFtits"



def DATABASE():
    connection = pymysql.connect(host='sdecheap.clcutdgbykfx.us-east-1.rds.amazonaws.com',
                                 user='derek', # TODO: Make this better
                                 password='bojangles1', # TODO: Make this better
                                 db='SDECheap',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection


def boostScore(_onyen):
    connection = DATABASE()
    cursor = connection.cursor()
    sql = "update SDECheap.USERS set score = score + 1 where onyen = \"%s\";" % (_onyen)
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return None


def registerCourse(_onyen, _password, _course, _score, _success, _referringOnyen=None):
    """
    Check if the user has already registered for this course. If so, 
    reject them. Get their score from this query to use later.
    If not, check their current score and add them with a new score.
    Finally, give more points to the referring onyen.
    """
    # TODO: See if they have a higher score than 0
    # Connect to the database with 'connection'
    # TODO: Encrypt onyen and password
    connection = DATABASE()
    cursor = connection.cursor()

    # Encrypts the onyen. It looks like this b'\x23 etc'
    #TODO _score = getScore(_onyen)
    # _password = bojangles.encrypt_password(_password, chickfila)

    cursor.execute("select * from SDECheap.USERS where onyen = \"%s\" and course = \"%s\"" % (_onyen, _course))


    if len(cursor.fetchall()) != 0:
        print("INFO: %s is already registered for %s. Not adding shit." % (_onyen, _course))
        return False
    
    else:
        cursor = connection.cursor()
        sql = "insert into SDECheap.USERS (onyen, password, course, score, success, mobile) VALUES (\"%s\", \"%s\", \"%s\", %s, %s, \"NO MOBILE\");" % (_onyen, _password, _course, _score, _success)
        cursor.execute(sql)
        connection.commit()

        if _referringOnyen == None: 
            pass  
        else: 
            boostScore(_referringOnyen)

    connection.commit()
    connection.close()

    return None

# registerCourse("Bojangles", "bojangles6'", "AAAD 101-002", 1, 0)


def getNextUser(_course):
    """
    This method needs to be faster than greased lightning.
    Query all rows with the proper course and success == 0
    then use the weighting process to decide who gets the attempt. 
    Returns the onyen and password.
    """
    connection = DATABASE()

    cursor = connection.cursor()

    sql = "select * from SDECheap.USERS where course = \"%s\" and success = 0" % (_course)

    cursor.execute(sql)
    connection.commit()

    candidates = cursor.fetchall()



    hat = []

    if len(candidates) == 0:
        print("INFO: Zero candidates currently want %s" % _course)
        return None
    
    else:
        for candidate in candidates:

            for i in range(0, candidate["score"]):
                hat.append(candidate["onyen"])


        winner = random.choice(hat)
        print("INFO: Selecting %s for attempt of enrollment in %s!" % (winner, _course))

    for candidate in candidates:
        if candidate["onyen"] == winner:
            nextUser = candidate
            break
        else:
            continue

    connection.close()

    print(nextUser)

    return nextUser
# getNextUser("AAAD 101-001")


def markSuccess(_onyen, _course):
    """
    Change success from 0 to 1. E-mail them telling them they got in.
    # TODO: RESET REFERRAL COUNT
    """
    print("INFO: Marking enrollment success for onyen %s and course %s" % (_onyen, _course))
    
    connection = DATABASE()

    cursor = connection.cursor()

    sql = "update SDECheap.USERS set success = 1 where onyen = \"%s\" and course = \"%s\"" % (_onyen, _course)

    cursor.execute(sql)
    connection.commit()
    connection.close()

    return None


def removeClass(_onyen, _password, _course):
    """
    Removes the row with the provided _onyen 
    and _course.
    #TODO: If they're not tracking the course, do nothing
    """
    print("INFO: Marking success on %s for onyen %s" % (_course, _onyen))

    connection = DATABASE()

    cursor = connection.cursor()

    sql = "update SDECheap.USERS set success = 1 where onyen = \"%s\" and password = \"%s\"and course = \"%s\";" % (_onyen, _password, _course)

    cursor.execute(sql)
    connection.commit()
    connection.close()

    return None


def unregister(_onyen, _password):
    """
    Completely removes the given
    onyen from Swap Drop Enroll.
    # TODO: If they aren't in the database, do nothing
    """
    print("INFO: Removing %s from the database" % _onyen)

    connection = DATABASE()

    cursor = connection.cursor()

    sql = "update SDECheap.USERS set success = 1 where onyen = \"%s\" and pasword = \"%s\"" % (_onyen, _password)

    cursor.execute(sql)
    connection.commit()
    connection.close()

    return None














if __name__ == '__main__':
    app.run(debug=True)
