from board.utility import Loggable, log_method_call, make_error


class TaskListRequestHandler(Loggable):
    _db = None

    def __init__(self, db, logger):
        Loggable.__init__(self, logger=logger)
        self._debug_log("__init__() START")

        self._db = db

        self._debug_log("__init__() END")

    @log_method_call
    def get_request(self):
        return self._db.find_all(), 200

    @log_method_call
    def post_request(self, title):
        return self._db.insert(title), 201


class TaskRequestHandler(Loggable):
    _db = None

    def __init__(self, db, logger):
        Loggable.__init__(self, logger=logger)
        self._debug_log("__init() START")

        self._db = db

        self._debug_log("__init() END")

    @log_method_call
    def get_request(self, id):
        tasks = self._db.find(id)
        if 0 == len(tasks):
            self._error_log("Resource with id: %d not found!" % id)
            return make_error(404)

        return tasks[0], 200

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

        return tasks[0], 200

    @log_method_call
    def delete_request(self, id):
        # these are not needed, delete should return an error if the id is invalid!
        tasks = self._db.find(id)
        if 0 == len(tasks):
            return make_error(404)

        self._db.delete(id)
        return tasks[0], 200
