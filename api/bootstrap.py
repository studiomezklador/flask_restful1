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

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile(configFile)

