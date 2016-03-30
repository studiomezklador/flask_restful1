import os
from api.__init__ import ai, app, db, parentdir
from flask_restful import reqparse, abort, Resource, fields, marshal
from flask import g, jsonify, request, make_response
# from models.auth import User, Role

@app.before_request
def clientIp():
    g.client_ip = request.remote_addr


class HelloWorld(Resource):
    def get(self):
        ip = request.remote_addr
        return jsonify(dict(version='1.0', your_ip=g.client_ip, code=200, status=True, evil=None))

"""
TODOS = {
        'todo1': {'task': 'run something', 'status': None, 'active': True, 'integer': 5, 'float':45.123},
        'todo2': {'task': 'build a box', 'status': [], 'active': False, 'integer':101, 'float':.257},
    'todo3': {'task': 'busy-awared', 'status': ['yank', 'mystic'], 'active': True, 'integer':15, 'float':None},

}
"""

TODOS = [
        {'id': 1, 'task': 'run something', 'status': None, 'active': True, 'integer': 5, 'float':45.123},
        {'id': 2, 'task': 'build a box', 'status': [], 'active': False, 'integer':101, 'float':.257},
        {'id': 3, 'task': 'busy-awared', 'status': ['yank', 'mystic'], 'active': True, 'integer':15, 'float':None},
]

todo_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'status': fields.List,
    'active': fields.Boolean,
    'integer': fields.Integer,
    'float': fields.Float,
    'uri': fields.Url('todo')

}


def error_todo_not_find(todo_id):
    if int(todo_id) > len(TODOS) or (todo_id) < 0:
        abort(404, message="Todo {} does not exist".format(todo_id))

parser= reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('p', type=int, location='args')

class Todo(Resource):
    def get(self, todo_id):
        error_todo_not_find(todo_id - 1)
        return TODOS[todo_id - 1]

    def delete(self, todo_id):
        error_todo_not_find(todo_id)
        del TODOS[todo_id]
        return dict(msg="{} removed".format(todo_id)), 203

    def put(self, todo_id):
        args = parser.parse_args()
        tasks = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

class TodoList(Resource):
    def get(self):
        args = parser.parse_args()
        paginate = args['p']
        if paginate and paginate <= len(TODOS):
            return dict(per_page=paginate,
                        total=len(TODOS),
                        remain=len(TODOS) - paginate,
                        result=list(TODOS.items())[0:paginate])
        return marshal(TODOS, todo_fields), 200

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo{}'.format(todo_id)
        TODOS[todo_id] = {'task': args['task']}
        return make_response(jsonify(dict(result=TODOS[todo_id],
                                          status="inserted")), 201)

ai.add_resource(HelloWorld, '/')
ai.add_resource(TodoList, '/todos')
ai.add_resource(Todo, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
