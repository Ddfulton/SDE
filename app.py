# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
import json
import subprocess
import email_driver


app = Flask(__name__)



@app.route('/', methods=["POST", "GET"])

def index():
    if request.method == "POST":
    	print("GOT THE MOTHATFUCKING SENDGRID. HERE IT IS %s" % json.loads(request.data))
    	
    	# try:
    	# 	goods = request.data
    	# except:
    	# 	print("goods = request.data did not work :(")
    	

    	# try:
    	# 	goods = request.data.decode('utf-8')
    	# except:
    	# 	print("goods = request.data.decode('utf-8')")

    	
    	email_driver.send_email('fulton.derek@gmail.com', 'You got a post', '%s' % request.data.decode('utf-8'))
    else:
        pass
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)