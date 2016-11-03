### General Depdencies ###
import sendgrid
import os
import json
import base64
from flask import request
import subprocess
import smtplib

### API Dependencies ###
import SDEClient

# TODO Database query to remove from classchecker

def enroll(onyen, password, course):
    """
    Calls driver.rb to login to course.
    Example: drive('kanye', 'kim', 'RAPP 101-001')
    """
    print("INFO: Calling enroll for %s for %s" % (onyen, course))
    args = ['ruby', 'driver.rb', onyen, password, course]
    print(subprocess.call(args))


def verify_onyen(onyen, password):
    """
    Returns YE for a success and NO for a failure
    """

    print("INFO: Attempting to authenticate Onyen %s" % onyen)

    p = subprocess.Popen(["ruby", "verifyOnyen.rb", onyen, password], stdout=subprocess.PIPE)

    out, err = p.communicate()

    result = out[-3:].decode('utf-8')[0:2]

    if result == "YE":
        return True 

    else:
        return False


def class_checker(course):
    """
    Signs special sendgrid account up for ClassChecker
    Example: class_checker('CHEM 262-001')
    """

    args = ['ruby', 'classchecker.rb', course]
    subprocess.call(args)


def untrack(course):
    """
    Works just like class_checker, but untracks the course instead.
    """

    args = ['ruby', 'untrack.rb', course]
    subprocess.call(args)


# def send_email(recipient, subject, body, attachment=None):
#     """
#     Sends an e-mail without an attachment using Sendgrid's V3 Web API
#     Example: send_email('kanye.west@live.unc.edu, 'Eighteen years', 'She got yo ass for eighteen years'
#     """

#     sg = sendgrid.SendGridAPIClient(apikey = "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")

#     if attachment != None: 
        
#         encoded_image = base64.b64encode(open(attachment, "rb").read()).decode('utf-8')

#         data = {
#             "personalizations": [
#                 {
#                     "to": [
#                         {
#                             "email": recipient
#                         }
#                     ],
#                     "subject": subject
#                 }
#             ],
#             "from": {
#                 "email": "swap@drop.enroll"
#             },
#             "content": [
#                 {
#                     "type": "text/plain",
#                     "value": body
#                 }
#             ],
#             "attachments": [
#             {
#                 "content": encoded_image,  
#                 "filename": attachment, 
#                 "name": "EnrollmentResult", 
#                 "type": "png"
#             }
#             ],
#         }

#     else:
        
#         data = {
#             "personalizations": [
#                 {
#                     "to": [
#                         {
#                             "email": recipient
#                         }
#                     ],
#                     "subject": subject
#                 }
#             ],
#             "from": {
#                 "email": "swap@drop.enroll"
#             },
#             "content": [
#                 {
#                     "type": "text/plain",
#                     "value": body
#                 }
#             ]
#         }


#     response = sg.client.mail.send.post(request_body=data)

#     return response.status_code, response.body, response.headers

#     print("SEND EMAIL TO %s" % data[personalizations][0]["to"])


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


def send_email_attachment(to, text, subject, attachment):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
     
    fromaddr = "registerer69@gmail.com"
    toaddr = to
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
     
    body = text
     
    msg.attach(MIMEText(body, 'plain'))
     
    filename = attachment
    attachment = open(attachment, "rb")
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "bojangles1")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def send_email_plain(recipient, subject, text):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
     
     
    fromaddr = "registerer69@gmail.com"
    toaddr = recipient
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
     
    body = text
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "bojangles1")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()



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

