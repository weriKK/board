from sqlalchemy import Table
from board.utility import Loggable, log_method_call


# [TODO kova]: error handling?!
#              debug logging each function + sql statement
class TasksTable(Loggable):
    _table = None

    def __init__(self, dbm, logger=None):
        Loggable.__init__(self, logger=logger)
        self._debug_log("__init__() START")
        self._table = Table('tasks', dbm.get_db_metadata('board'), autoload=True)
        self._debug_log("__init__() END")

    @log_method_call
    def _build_tasks(self, result):
        tasks = []
        for row in result:
            tasks.append({ 'id': row[0], 'title': row[1], 'isDone': row[2] })
            # self._debug_log(tasks[-1])

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
        self._debug_log('INSERT new id: %d' % new_id)

        return new_id

    @log_method_call
    def update(self, task):
        result = self._table.update(task['id'] == self._table.c.id).execute(isDone=task['isDone'], title=task['title'])
        self._debug_log('UPDATE matched: %d' % result.rowcount)

    @log_method_call
    def delete(self, task):
        result = self._table.delete(task['id'] == self._table.c.id).execute()
        self._debug_log('DELETE matched: %d' % result.rowcount)
