import os, sys
from flask import Flask, jsonify
from flask_restful import Api, HTTPException
from flask.ext.sqlalchemy import SQLAlchemy

__version__ = "1.0"
__author__ = "Mzk"

parentdir = os.path.dirname(__file__)

configFile = os.path.join(parentdir, 'common', 'config.py')

app = Flask(__name__)
ai = Api(app, prefix='/v1')

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile(configFile)

db = SQLAlchemy(app)

"""
Errors
FROM: http://stackoverflow.com/questions/13773862/api-in-flask-returns-json-but-html-exceptions-break-my-json-client:#answer-13793320
"""


@app.errorhandler(404)
def content_not_found(e):
    return jsonify(dict(error=1,
                        message="{}".format(e))), 404


@app.errorhandler(500)
def out_of_service(e):
    return jsonify(dict(error=0,
                        message="{}".format(e))), 500
