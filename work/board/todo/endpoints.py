from flask import Blueprint
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.restful import fields, marshal

from .models import TasksTable
from .handlers import TaskListRequestHandler, TaskRequestHandler


# absolute=True ensures that the generated Urls will have the hostname included
TODO_OUTPUT_FIELDS = {
    'title': fields.String,
    'isDone': fields.Boolean,
    'uri': fields.Url('todo_blueprint.task', absolute=True)
}


# [TODO KOVA]: cant log this method without a logger! Resource classes have no loggers
# @log_method_call
def format_todo_response(self, wrapper, output, status_code):
    if status_code < 200 or 300 <= status_code:
        return output

    # if output is a dictionary { .. }
    if isinstance(output, dict):
        return {wrapper: marshal(output, TODO_OUTPUT_FIELDS)}

    # if output is a list (of dictionaries) [ {}, {}.. ]
    elif isinstance(output, list):
        return {wrapper: map(lambda t: marshal(t, TODO_OUTPUT_FIELDS), output)}

    else:
        return None

todo_blueprint = Blueprint('todo_blueprint', __name__)


# This decorator makes the function execute when the blueprint is registered.
@todo_blueprint.record
def init_db_on_blueprint_registration(setup_state):
    db = TasksTable(setup_state.app.dbm, setup_state.app.logger)
    TaskListAPI.inject_request_handler(TaskListRequestHandler(db, setup_state.app.logger))
    TaskListAPI.inject_response_formatter(format_todo_response)

    TaskAPI.inject_request_handler(TaskRequestHandler(db, setup_state.app.logger))
    TaskAPI.inject_response_formatter(format_todo_response)
    return

todo_api = Api(todo_blueprint)

# from board.auth import basicAuth


# [Todo kova]: try catch exceptions and throw abort(500, {'message':'custom message'}) 500 errors!
# [Todo kova]: ^ Instead of the above, try using flask custom error handling!!!
# [TODO kova]: throw exception if request handler is not injected?
class TaskListAPI(Resource):
    # decorators = [basicAuth.login_required]

    _request_handler = None
    _format_response = None

    def __init__(self):
        super(TaskListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')

    @classmethod
    def inject_request_handler(cls, handler):
        cls._request_handler = handler

    @classmethod
    def inject_response_formatter(cls, formatter):
        cls._format_response = formatter

    # Get the complete Task List
    def get(self):
        output, status = self._request_handler.get_request()
        return self._format_response('tasks', output, status), status

    # Create a new Task
    def post(self):
        args = self.reqparse.parse_args()
        output, status = self._request_handler.post_request(args['title'])
        return self._format_response('task', output, status), status


class TaskAPI(Resource):
    _request_handler = None
    _format_response = None

    def __init__(self):
        super(TaskAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('isDone', type=bool, location='json')

    @classmethod
    def inject_request_handler(cls, request_handler):
        cls._request_handler = request_handler

    @classmethod
    def inject_response_formatter(cls, formatter):
        cls._format_response = formatter

    # Get a single Task
    def get(self, id):
        output, status = self._request_handler.get_request(id)
        return self._format_response('task', output, status), status

    # Modify/Update a single Task
    def put(self, id):
        output, status = self._request_handler.put_request(id, self.reqparse.parse_args())
        return self._format_response('task', output, status), status

    # Delete a single Task
    def delete(self, id):
        output, status = self._request_handler.delete_request(id)
        return self._format_response('task', output, status), status

todo_api.add_resource(TaskListAPI, '/tasks', endpoint='tasklist')
todo_api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint='task')
