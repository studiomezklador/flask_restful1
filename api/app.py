from __init__ import ai, app
from flask_restful import Resource
from flask import jsonify


class HelloWorld(Resource):
    def get(self):
        return jsonify(dict(hello='World', code=200, status=True, evil=None))

ai.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
