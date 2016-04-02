form flask_restful import Resource, marshal, marshal_with

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

