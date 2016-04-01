# from collections import OrderedDict
import os
from bootstrap import ai, app, db, parentdir
from flask_restful import reqparse, abort, Resource, fields, marshal_with, marshal
from flask import g, jsonify, request, make_response
# from models.auth import User, Role

@app.before_request
def clientIp():
    g.client_ip = request.remote_addr

ROOT = app.root_path

class HelloWorld(Resource):
    def get(self):
        ip = request.remote_addr
        return jsonify(dict(version='1.0',
                            abs_path=ROOT,
                            your_ip=g.client_ip,
                            code=200))

TODOS = {
        1: {'task': 'run something', 'status': None, 'active': True,},
        2: {'task': 'build a box', 'status': [], 'active': False, },
        3: {'task': 'busy-awared', 'status': ['yank', 'mystic'], 'active': True},
}

TODAS = [
        {'todo_id': 1, 'task': 'run something', 'status': None, 'active': False},
        {'todo_id': 2, 'task': 'build a box', 'status': [], 'active': False},
        {'todo_id': 3, 'task': 'busy-awared', 'status': ['yank', 'mystic'], 'active': True}
]


class TodoObj(object):
    """
    Dynamic properties for this class, according to keys from a dict.
    FROM: http://goodcode.io/articles/python-dict-object/
    """

    def __init__(self, d):
        self.__dict__ = d

    def __getattribute__(self, key):
        return object.__getattribute__(self, key)
    


class TodoContainer(object):
    def __init__(self, todosList):
        self.todos_obj = [TodoObj(x) for x in todosList]

    def getBy(self, **kw):
        for prop, value in kw.items():
            for it in self.todos_obj:
                if getattr(it, prop) == value:
                    return it
        return False

    def all(self):
        return [vars(obj) for obj in self.todos_obj]


tc = TodoContainer(TODAS)


todo_fields = {
    'task': fields.String,
    'active': fields.Boolean,
    'uri': fields.Url('todo', absolute=True)
}


def error_todo_not_find(todo_id):
    if int(todo_id) > len(tc.todos_obj) or (todo_id) < 0:
        abort(404, message="Todo {} does not exist".format(todo_id))

parser= reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('pp', type=int, location='args')
parser.add_argument('p', type=int, location='args')


class Todo(Resource):
    def get(self, todo_id, **kwargs):
        res = tc.getBy(todo_id=todo_id)
        if not res:
            return error_todo_not_find(todo_id)
        return marshal(res, todo_fields)
    
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
    @marshal_with(todo_fields)
    def get(self):
        args = parser.parse_args()
        paginate = args['pp']
        target_page = args['p']
        if target_page is None:
            target_page = 0

        if paginate and paginate <= len(tc.todos_obj):
            return dict(per_page=paginate,
                        total=len(tc.todos_obj),
                        remain=len(tc.todos_obj) - paginate,
                        result=list(tc.all())[0:paginate])
        result = tc.all()
        return result, 200

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo{}'.format(todo_id)
        TODOS[todo_id] = {'task': args['task']}
        return make_response(jsonify(dict(result=TODOS[todo_id],
                                          status="inserted")), 201)

ai.add_resource(HelloWorld, '/')
ai.add_resource(TodoList, '/todos', endpoint='todos')
ai.add_resource(Todo, '/todo/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
