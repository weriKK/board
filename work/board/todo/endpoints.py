from flask import Blueprint
from flask.ext.restful import Api, Resource, reqparse

from .models import TasksTable
from .handlers import TaskListRequestHandler, TaskRequestHandler


todo_blueprint = Blueprint('todo_blueprint', __name__)


# This decorator makes the function execute when the blueprint is registered.
@todo_blueprint.record
def init_db_on_blueprint_registration(setup_state):
    db = TasksTable(setup_state.app.dbm, setup_state.app.logger)
    TaskListAPI.inject_request_handler(TaskListRequestHandler(db, setup_state.app.logger))
    TaskAPI.inject_request_handler(TaskRequestHandler(db, setup_state.app.logger))
    return

todo_api = Api(todo_blueprint)

# from board.auth import basicAuth


# [Todo kova]: try catch exceptions and throw abort(500, {'message':'custom message'}) 500 errors!
# [Todo kova]: ^ Instead of the above, try using flask custom error handling!!!
# [TODO kova]: throw exception if request handler is not injected?
class TaskListAPI(Resource):
    # decorators = [basicAuth.login_required]

    _request_handler = None

    def __init__(self):
        super(TaskListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')

    @classmethod
    def inject_request_handler(cls, request_handler):
        cls._request_handler = request_handler

    # Get the complete Task List
    def get(self):
        return self._request_handler.get_request()

    # Create a new Task
    def post(self):
        args = self.reqparse.parse_args()
        return self._request_handler.post_request(args['title'])


class TaskAPI(Resource):
    _request_handler = None

    def __init__(self):
        super(TaskAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('isDone', type=bool, location='json')

    @classmethod
    def inject_request_handler(cls, request_handler):
        cls._request_handler = request_handler

    # Get a single Task
    def get(self, id):
        return self._request_handler.get_request(id)

    # Modify/Update a single Task
    def put(self, id):
        return self._request_handler.put_request(id, self.reqparse.parse_args())

    # Delete a single Task
    def delete(self, id):
        return self._request_handler.delete_request(id)

todo_api.add_resource(TaskListAPI, '/tasks', endpoint='tasklist')
todo_api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint='task')
