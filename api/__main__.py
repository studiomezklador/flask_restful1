from __init__ import ai, app
from flask_restful import reqparse, abort, Resource
from flask import jsonify, request

class HelloWorld(Resource):
    def get(self):
        ip = request.remote_addr
        return jsonify(dict(hello='World', ip=ip, code=200, status=True, evil=None))


TODOS = {
        'todo1': {'task': 'run something', 'status': None, 'active': True, 'integer': 5, 'float':45.123},
        'todo2': {'task': 'build a box', 'status': [], 'active': False, 'integer':101, 'float':.257},
    'todo3': {'task': 'busy-awared', 'status': ['yank', 'mystic'], 'active': True, 'integer':15, 'float':.4567},

}

def error_todo_not_find(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} does not exist".format(todo_id))

parser= reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('p', type=int, location='args')

class Todo(Resource):
    def get(self, todo_id):
        error_todo_not_find(todo_id)
        return TODOS[todo_id]

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
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo{}'.format(todo_id)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

ai.add_resource(HelloWorld, '/')
ai.add_resource(TodoList, '/todos')
ai.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
