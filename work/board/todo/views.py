from flask import Blueprint, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from .models import db_get_tasks, db_update_task, db_insert_task, db_delete_task
from .log import logger


todo_dbm = None
todo_blueprint = Blueprint('todo_blueprint', __name__)

# restapi -> get post put delete (this file), but only gathering / parsing the request arguments, then passing them to the handler
# handler -> responsible for all the work on the request arguments, basically a controller (possibly as a class with
#            handler functions for get/put/delete/etc)
# models  -> responsible for any kind of database operation on the data, the handler uses it
#
# basically: request arrives -> restapi processes the arguments -> handler does the work, possibly using models -> returns
#            response to restapi
#
# similar to view/controller/model, restapi/handler/models


# This decorator makes the function execute when the blueprint is registered.
@todo_blueprint.record
def init_db_on_blueprint_registration(setup_state):
    global todo_dbm
    todo_dbm = setup_state.app.dbm
    return

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
        return {'tasks': map(lambda t: marshal(t, task_fields), db_get_tasks(todo_dbm))}

    # Create a new Task
    def post(self):
        args = self.reqparse.parse_args()

        task = {
            'id': db_insert_task(args['title'], todo_dbm),
            'title': args['title'],
            'isDone': False
        }

        return { 'task': marshal(task, task_fields) }, 201


class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('isDone', type=bool, location='json')
        super(TaskAPI, self).__init__()

    # Get a single Task
    def get(self, id):
        tasks = db_get_tasks(todo_dbm, id)
        if 0 == len(tasks):
            abort(404)

        return {'task': marshal(tasks[0], task_fields)}

    # Modify/Update a single Task
    def put(self, id):
        tasks = db_get_tasks(todo_dbm, id)
        if 0 == len(tasks):
            abort(404)

        # Parse the put request task object, update those tasks fields
        # which where changed, keep the rest untouched, then update the db!
        task = tasks[0]
        args = self.reqparse.parse_args()
        # [ TODO kova]: only update the db if something changed?!
        for k, v in args.iteritems():
            if v is not None:
                task[k] = v

        db_update_task(task, todo_dbm)

        return {'task': task}

    # Delete a single Task
    def delete(self, id):
        # these are not needed, delete should return an error if the id is invalid!
        tasks = db_get_tasks(todo_dbm, id)
        if 0 == len(tasks):
            abort(404)

        db_delete_task(tasks[0], todo_dbm)
        return { 'result': True }

todo_api.add_resource(TaskListAPI, '/tasks', endpoint='tasklist')
todo_api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint='task')
