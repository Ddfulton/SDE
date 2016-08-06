# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
import json
import subprocess
import email_driver
import simplejson


app = Flask(__name__)



@app.route('/', methods=["GET"])

def index():
    return render_template("index.html")

@app.route('/parse', methods=["POST"])
def parser():
	# Required response to SendGrid.com’s Parse API
	print("GOT THE SENDGRID")

	# Consume the entire email
	envelope = simplejson.loads(request.form.get('envelope'))
	print(envelope)

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

if __name__ == '__main__':
    app.run(debug=True)