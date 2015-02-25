from sqlalchemy import Table
from board.utility import log_method_call


# [TODO kova]: error handling?!
#              debug logging each function + sql statement
#              logging decorator maybe?
class TasksTable:
    _table = None
    _logger = None

    def __init__(self, dbm, logger=None):
        self._table = Table('tasks', dbm.get_db_metadata('board'), autoload=True)
        self._logger = logger
        self._log("__init__")

    def _log(self, msg):
        if self._logger is not None:
            self._logger.debug("%s: %s", self.__class__, msg)

    @log_method_call
    def _build_tasks(self, result):
        tasks = []
        for row in result:
            tasks.append({ 'id': row[0], 'title': row[1], 'isDone': row[2] })
            self._log(tasks[-1])

        return tasks

    @log_method_call
    def find_all(self):
        result = self._table.select().execute()
        return self._build_tasks(result)

    @log_method_call
    def find(self, task_id):
        result = self._table.select(task_id == self._table.c.id).limit(1).execute()
        return self._build_tasks(result)

    @log_method_call
    def insert(self, title):
        result = self._table.insert().execute(title=title, isDone=0)
        new_id = result.inserted_primary_key[0]
        self._log('INSERT new id: %d' % new_id)

        return new_id

    @log_method_call
    def update(self, task):
        result = self._table.update(task['id'] == self._table.c.id).execute(isDone=task['isDone'], title=task['title'])
        self._log('UPDATE matched: %d' % result.rowcount)

    @log_method_call
    def delete(self, task):
        result = self._table.delete(task['id'] == self._table.c.id).execute()
        self._log('DELETE matched: %d' % result.rowcount)
