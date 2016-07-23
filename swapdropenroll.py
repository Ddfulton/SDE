# -*- coding: utf-8 -*-
from flask import Flask, render_template, request 
from werkzeug.datastructures import ImmutableMultiDict
import json, driver
import subprocess


app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])

def index():
    if request.method == "POST":
        goods = request.data.decode('utf-8')
        goods = json.loads(goods) # solid dictionary
        print(goods)
    else:
        pass
    return render_template("index.html")




if __name__ == '__main__':
    app.run(debug=True)

