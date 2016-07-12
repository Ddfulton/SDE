# -*- coding: utf-8 -*-
from flask import Flask, render_template, request 
from werkzeug.datastructures import ImmutableMultiDict
import json


app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html")




if __name__ == '__main__':
    app.run(debug=True)

