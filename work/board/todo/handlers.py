from flask.ext.restful import fields, marshal
from board.utility import Loggable, log_method_call, make_error


class TaskListRequestHandler(Loggable):
    _db = None
    _task_fields = None

    def __init__(self, db, logger):
        Loggable.__init__(self, logger=logger)
        self._debug_log("__init__() START")

        self._db = db

        # absolute=True ensures that the generated Urls will have the hostname included
        self._task_fields = {
            'title': fields.String,
            'isDone': fields.Boolean,
            'uri': fields.Url('todo_blueprint.task', absolute=True)
        }

        self._debug_log("__init__() END")

    @log_method_call
    def get_request(self):
        return {'tasks': map(lambda t: marshal(t, self._task_fields), self._db.find_all())}, 200

    @log_method_call
    def post_request(self, title):
        task = {
            'id': self._db.insert(title),
            'title': title,
            'isDone': False
        }

        return { 'task': marshal(task, self._task_fields) }, 201


class TaskRequestHandler(Loggable):
    _db = None
    _task_fields = None

    def __init__(self, db, logger):
        Loggable.__init__(self, logger=logger)
        self._debug_log("__init() START")

        self._db = db

        # absolute=True ensures that the generated Urls will have the hostname included
        self._task_fields = {
            'title': fields.String,
            'isDone': fields.Boolean,
            'uri': fields.Url('todo_blueprint.task', absolute=True)
        }

        self._debug_log("__init() END")

    @log_method_call
    def get_request(self, id):
        tasks = self._db.find(id)
        if 0 == len(tasks):

            return make_error(404)

        return {'task': marshal(tasks[0], self._task_fields)}

    @log_method_call
    def put_request(self, id, args=None):
        tasks = self._db.find(id)
        if 0 == len(tasks):
            return make_error(404)

        # Parse the put request task object, update those tasks fields
        # which where changed, keep the rest untouched, then update the db!

        # [ TODO kova]: only update the db if something changed?!
        for k, v in args.iteritems():
            if v is not None:
                tasks[0][k] = v

        self._db.update(tasks[0])

        return {'task': tasks[0]}, 200

    @log_method_call
    def delete_request(self, id):
        # these are not needed, delete should return an error if the id is invalid!
        tasks = self._db.find(id)
        if 0 == len(tasks):
            return make_error(404)

        self._db.delete(tasks[0])
        return { 'result': True }, 200
