from collections import OrderedDict
from flask_restful import fields, marshal_with, Resource, Api
from flask import Flask

app = Flask(__name__)

api = Api(app)

# for Url: define the strict endpoint to target
res_fields = {
        'task': fields.String,
        'uri': fields.Url('todo_it', absolute=True)
}

# the class must have a strict id named (todo_id, for instance)
class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task
        self.status = False

# Must return ONE object, with the same attribut in kwargs (todo_id)
class Todo(Resource):
    @marshal_with(res_fields)
    def get(self, **kwargs):
        obj = TodoDao(todo_id='todo1', task='Do not forget the milk!')
        print(obj, type(obj))
        return obj

# Must request the same variable as class property!
api.add_resource(Todo, '/<string:todo_id>', endpoint='todo_it')

if __name__ == '__main__':
    app.run(debug=True)
