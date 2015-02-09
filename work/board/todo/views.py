from flask import Blueprint, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from .models import tasks, db_save_task
from .log import logger

todo_blueprint = Blueprint('todo_blueprint', __name__)
todo_api = Api(todo_blueprint)

# from board.auth import basicAuth

# absolute=True ensures that the generated Urls will have the hostname included
task_fields = {
    'title': fields.String,
    'isDone': fields.Boolean,
    'uri': fields.Url('todo_blueprint.task', absolute=True)
}


class TaskListAPI(Resource):
    # decorators = [basicAuth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')
        super(TaskListAPI, self).__init__()

    # Get the complete Task List
    def get(self):
        return {'tasks': map(lambda t: marshal(t, task_fields), tasks)}

    # Create a new Task
    def post(self):
        args = self.reqparse.parse_args()

        task = {
            'id': 0 if (0 == len(tasks)) else tasks[-1]['id'] + 1,
            'title': args['title'],
            'isDone': False
        }

        tasks.append(task)
        return { 'task': marshal(task, task_fields) }, 201


class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('isDone', type=bool, location='json')
        super(TaskAPI, self).__init__()

    # Get a single Task
    def get(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if 0 == len(task):
            abort(404)

        return {'task': marshal(task[0], task_fields)}

    # Modify/Update a single Task
    def put(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if 0 == len(task):
            abort(404)

        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if None != v:
                task[k] = v

        db_save_task(task)

        return {'task': task}

    # Delete a single Task
    def delete(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        if 0 == len(task):
            abort(404)

        tasks.remove(task[0])
        return { 'result': True }

todo_api.add_resource(TaskListAPI, '/tasks', endpoint='tasklist')
todo_api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint='task')
