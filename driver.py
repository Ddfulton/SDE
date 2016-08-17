import sendgrid
import os
import json
import base64
from flask import request
import subprocess
import zeep


# TODO Database query to remove from classchecker

def enroll(onyen, password, course):
    """
    Calls driver.rb to login to course.
    Example: drive('kanye', 'kim', 'RAPP 101-001')
    """
    print("INFO: Calling enroll for %s for %s" % (onyen, course))
    args = ['ruby', 'driver.rb', onyen, password, course]
    print(subprocess.call(args))


def class_checker(course):
    """
    Signs special sendgrid account up for ClassChecker
    Example: class_checker('CHEM 262-001')
    """

    args = ['ruby', 'classchecker.rb', course]
    subprocess.call(args)


def send_email(recipient, subject, body, attachment=None):  #TODO debug image shit
    """
    Sends an e-mail without an attachment using Sendgrid's V3 Web API
    Example: send_email('kanye.west@live.unc.edu, 'Eighteen years', 'She got yo ass for eighteen years'
    """
    ###TODO STORE API KEY SOMEWHERE MORE SECURE AND FETCH IT WITH ZEEP###
    sg = sendgrid.SendGridAPIClient(apikey='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')



    if attachment != None: 
        
        
        encoded_image = base64.b64encode(open(attachment, "rb").read()).decode('utf-8')

        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": recipient
                        }
                    ],
                    "subject": subject
                }
            ],
            "from": {
                "email": "swap@drop.enroll"
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": body
                }
            ],
            "attachments": [
            {
                "content": encoded_image,  
                "filename": "ddfulton_ECON 400-001_2016-08-14 11:40:50 -0400.png", 
                "name": "THE_PICTURE", 
                "type": "png"
            }
            ],
        }

    else:
        
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": recipient
                        }
                    ],
                    "subject": subject
                }
            ],
            "from": {
                "email": "swap@drop.enroll"
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": body
                }
            ]
        }


    response = sg.client.mail.send.post(request_body=data)

    return response.status_code, response.body, response.headers

    print("SEND EMAIL TO %s" % data[personalizations][0]["to"])


def parse_email(envelope):
    """
    Takes a sendgrid inbound parse e-mail object. Returns from, to, subject, body and status.
    Status is a string which is either "open", "closed" or "wait list".
    """

    to_address = envelope['to'][0]
    from_address = envelope['from']
    print("From: %s" % (from_address))

    subject = request.form.get('subject')
    text = request.form.get('text')
    print("Subject is %s" % subject)
    print("Text is %s" % text)

    course, status = parse_body(text)

    return from_address, to_address, subject, text, course, status


def parse_body(text):
    """
    Reads an e-mail from classchecker and returns the course and status so
    it's ready to go for the driver.
    """

    if "to open" in text.lower():
        status = "open"

    elif "wait list" in text.lower():
        status = "wait list"

    elif "to closed" in text.lower():
        status = "closed"

    else:
        status = "not sendgrid"


    if "has changed from" in text.lower(): # Probably from coursicle

        if text[8] == "H": # Honors class
            course = text[0:13]

        else:
            course = text[0:12]

    else:
        course = None

    return course, status

