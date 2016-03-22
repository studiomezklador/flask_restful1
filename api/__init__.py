from flask import Flask, jsonify
from flask_restful import Api

# from api.resources.foo import Foo
# from api.resources.bar import Bar

app = Flask(__name__)
ai = Api(app)


app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False