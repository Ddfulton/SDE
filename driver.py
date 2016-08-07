import sendgrid
import os
import json
import base64
from flask import request
import subprocess


# TODO Database query to remove from classchecker

def drive(onyen, password, course):
    """
    Calls driver.rb to login to course.
    Example: drive('kanye', 'kim', 'RAPP 101-001')
    """

    args = ['ruby', 'driver.rb', onyen, password, course]
    subprocess.call(args)


def class_checker(course):
    """
    Signs special sendgrid account up for ClassChecker
    Example: class_checker('CHEM 262-001')
    """

    args = ['ruby', 'classchecker.rb', course]
    subprocess.call(args)


def send_email(recipient, subject, body):  # TODO debug image shit
    """
    Sends an e-mail without an attachment using Sendgrid's V3 Web API
    Example: send_email('kanye.west@live.unc.edu, 'Eighteen years', 'She got yo ass for eighteen years'
    """

    sg = sendgrid.SendGridAPIClient(apikey='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')

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
    }

    response = sg.client.mail.send.post(request_body=data)

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return response.status_code, response.body, response.headers


def parse_email(envelope):
    """
    Parses an email object with:
    envelope = simplejson.loads(request.form.get('envelope'))
    Processes that envelope to get to_address, from_address, text and subject.
    """

    to_address = envelope['to'][0]
    from_address = envelope['from']
    print("From: %s" % (from_address))

    subject = request.form.get('subject')
    text = request.form.get('text')
    print("Subject is %s" % subject)
    print("Text is %s" % text)
    print("Reached end fo parse_email function")

    return from_address, to_address, subject, text
