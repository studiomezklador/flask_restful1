from flask_restful import abort, Resource, reqparse, fields, marshal, marshal_with
from .todotools import TodoContainer
from models.todos import TODAS

todo_fields = {
    'task': fields.String,
    'active': fields.Boolean,
    'uri': fields.Url('todo', absolute=True)
}


parser= reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('pp', type=int, location='args')
parser.add_argument('p', type=int, location='args')

tc = TodoContainer(TODAS)


def error_todo_not_find(todo_id):
    if int(todo_id) > len(tc.todos_obj) or (todo_id) < 0:
        abort(404, message="Todo {} does not exist".format(todo_id))


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

