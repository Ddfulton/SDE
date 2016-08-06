import sendgrid
import os
import json
import base64


def send_email(recipient, subject, body):
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
    # Get some header information
    to_address = envelope['to'][0]
    from_address = envelope['from']
    print("From: %s" % (from_address))

    # Now, onto the body
    text = request.form.get('text')
    html = request.form.get('html')
    subject = request.form.get('subject')
    print("Subject is %s" % (subject))
    print("Text is %s" % (text))

    return from_address, to_address, subject, body









#
#
# def add_to_classchecker(course):
#     # ADD THEM TO CLASSCHECKER
#
# def remove_from_classchecker(course):
#     # TAKE THE CLASS OUT OF CLASSCHECKER
#
# def parse_email(email_object):
#     # IF OPEN TO CLOSED
#         # DO NOTHING
#     # IF CLOSED TO OPEN
#         # QUERY DATABASE AND GET THE ONYENS AND SHIT AND DRIVE THEM IN WITH SUBPROCESS
#
