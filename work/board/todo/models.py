from sqlalchemy import Table


# [TODO kova]: error handling?!
#              debug logging each function + sql statement
#              logging decorator maybe?
class TasksTable:
    _table = None
    _logger = None

    def __init__(self, dbm, logger=None):
        self._table = Table('tasks', dbm.get_db_metadata('board'), autoload=True)
        self._logger = logger

    def _log(self, msg):
        if self._logger is not None:
            self._logger.debug("TasksTable - %s", msg)

    def _build_tasks(self, result):
        self._log("_build_tasks")
        tasks = []
        for row in result:
            tasks.append({ 'id': row[0], 'title': row[1], 'isDone': row[2] })
            print tasks[-1]

        return tasks

    def find_all(self):
        self._log("find_all")
        result = self._table.select().execute()

        return self._build_tasks(result)

    def find(self, task_id):
        self._log("find")
        result = self._table.select(task_id == self._table.c.id).limit(1).execute()

        return self._build_tasks(result)

    def insert(self, title):
        self._log("insert")
        result = self._table.insert().execute(title=title, isDone=0)
        new_id = result.inserted_primary_key[0]
        print 'INSERT new id: %d' % new_id

        return new_id

    def update(self, task):
        self._log("update")
        result = self._table.update(task['id'] == self._table.c.id).execute(isDone=task['isDone'], title=task['title'])
        print 'UPDATE matched: %d' % result.rowcount

    def delete(self, task):
        self._log("delete")
        result = self._table.delete(task['id'] == self._table.c.id).execute()
        print 'DELETE matched: %d' % result.rowcount
