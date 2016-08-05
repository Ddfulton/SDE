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

        "attachments": [
            {
                "content": base64.b64encode(b'fuckyou.png').decode('utf-8'),
                "filename": 'fuckyou.png',
                "type": 'png'
            }
        ]
    }

    response = sg.client.mail.send.post(request_body=data)

    print(response.status_code)
    print(response.body)
    print(response.headers)
    return response.status_code, response.body, response.headers













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
