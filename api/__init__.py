import os, sys
from flask import Flask, jsonify
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

__version__ = "1.0"
__author__ = "Mzk"

parentdir = os.path.dirname(__file__)

configFile = os.path.join(parentdir, 'common', 'config.py')

app = Flask(__name__)
ai = Api(app, prefix='/v1')
db = SQLAlchemy(app)

app.config.from_pyfile(configFile)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# app.config['JSON_AS_ASCII'] = False


app.config['SECRET_KEY'] = 'JDJiJDEwJHlaV043RkhadVNYQmlVYXhqSDVjLi41TFdFRy56OWdGMXpja3dvaFpQM3Nzb2hZWmhiNmpx'
