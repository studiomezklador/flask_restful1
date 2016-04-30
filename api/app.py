import os
from bootstrap import ai, app, db
from flask_restful import (
    reqparse,
    abort,
    Resource,
    fields,
    marshal_with,
    marshal)

from flask import g, jsonify, request, make_response
from tools.detect import UADetection as User_Agent

from resources.prototypes.todos import Todo, TodoList
# from models.auth import User, Role


@app.before_request
def clientIp():
    g.client_ip = request.remote_addr
    g.client_ua = User_Agent()

ROOT = app.root_path


class HelloWorld(Resource):
    def get(self):
        ip = request.remote_addr
        return jsonify(dict(version='1.0',
                            abs_path=ROOT,
                            your_ip=g.client_ip,
                            user_agent=g.client_ua.__dict__,
                            code=200))


ai.add_resource(HelloWorld, '/')
ai.add_resource(TodoList, '/todos', endpoint='todos')
ai.add_resource(Todo, '/todo/<int:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
