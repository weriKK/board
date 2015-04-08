from flask import Blueprint
from flask.ext.restful import Api, reqparse
from flask.ext.restful import fields, marshal

from .models import TasksTable
from .handlers import TaskListRequestHandler, TaskRequestHandler

from board.utility import BoardResource


LOGGER = None


# [TODO KOVA]: cant log this method without a logger! Resource classes have no loggers
# absolute=True ensures that the generated Urls will have the hostname included
TODO_OUTPUT_FIELDS = {
    'title': fields.String,
    'isDone': fields.Boolean,
    'uri': fields.Url('todo_blueprint.task', absolute=True)
}


def TODO_RESPONSE_FORMATTER(self, wrapper, output, status_code):
    if status_code < 200 or 300 <= status_code:
        LOGGER.debug("TODO_RESPONSE_FORMATTER: not 2xx Success")
        return output

    # if output is a dictionary { .. }
    if isinstance(output, dict):
        LOGGER.debug("TODO_RESPONSE_FORMATTER: dictionary output")
        return {wrapper: marshal(output, TODO_OUTPUT_FIELDS)}

    # if output is a list (of dictionaries) [ {}, {}.. ]
    elif isinstance(output, list):
        LOGGER.debug("TODO_RESPONSE_FORMATTER: list output")
        return {wrapper: map(lambda t: marshal(t, TODO_OUTPUT_FIELDS), output)}

    else:
        return None

todo_blueprint = Blueprint('todo_blueprint', __name__)

todo_api = Api(todo_blueprint)

# from board.auth import basicAuth


# [Todo kova]: try catch exceptions and throw abort(500, {'message':'custom message'}) 500 errors!
# [Todo kova]: ^ Instead of the above, try using flask custom error handling!!!
# [TODO kova]: throw exception if request handler is not injected?
class TaskListAPI(BoardResource):

    def __init__(self):
        super(TaskListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')

    # Get the complete Task List
    def get(self):
        output, status = self._request_handler.get_request()
        return self._format_response('tasks', output, status), status

    # Create a new Task
    def post(self):
        args = self.reqparse.parse_args()
        output, status = self._request_handler.post_request(args['title'])
        return self._format_response('task', output, status), status


class TaskAPI(BoardResource):

    def __init__(self):
        super(TaskAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('isDone', type=bool, location='json')

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


# This decorator makes the function execute when the blueprint is registered.
@todo_blueprint.record
def init_endpoints_on_blueprint_registration(setup_state):
    global LOGGER
    LOGGER = setup_state.app.logger
    LOGGER.debug("Todo Blueprint Registration START")

    db = TasksTable(setup_state.app.dbm, setup_state.app.logger)

    # [TODO Kova]: add logger to BoardResouce using make_api?! Then all of the methods can be logged!
    tasklistapi = TaskListAPI.make_api(TaskListRequestHandler(db, LOGGER), TODO_RESPONSE_FORMATTER)
    taskapi = TaskAPI.make_api(TaskRequestHandler(db, LOGGER), TODO_RESPONSE_FORMATTER)

    todo_api.add_resource(tasklistapi, '/tasks', endpoint='tasklist')
    todo_api.add_resource(taskapi, '/tasks/<int:id>', endpoint='task')

    LOGGER.debug("Todo Blueprint Registration END")
    return
