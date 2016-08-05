# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
import json
import subprocess
import email_driver


app = Flask(__name__)



@app.route('/', methods=["POST", "GET"])

def index():
    if request.method == "POST":
    	print("GOT THE MOTHATFUCKING SENDGRID")
    	print(goods)
        # goods = request.data.decode('utf-8')
        # goods = json.loads(goods) # solid dictionary
        # email_driver.send_email('ddfulton@live.unc.edu', 'Fuck you', 'Here are the goods:\n%s' % (goods))
        # print(goods)
    else:
        pass
    return render_template("index.html")




if __name__ == '__main__':
    app.run(debug=True)

