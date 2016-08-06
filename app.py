# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
import json
import subprocess
import email_driver


app = Flask(__name__)



@app.route('/', methods=["POST", "GET"])

def index():
    if request.method == "POST":
    	print("GOT THE MOTHATFUCKING SENDGRID. HERE IT IS %s" % request.data)
    	goods = request.data
    	goodsUTF8 = request.data.decode('utf-8')
    	
    	email_driver.send_email("Here are the goods for: request.data—%s\n request.data.decode('utf-8'):%s\n" % (goods, goodsUTF8)) 
    else:
        pass
    return render_template("index.html")




if __name__ == '__main__':
    app.run(debug=True)

