from sqlalchemy import Table


def db_get_tasks(dbm, task_id=None):
    meta = dbm.get_db_metadata('board')
    task_table = Table('tasks', meta, autoload=True)

    if 0 <= task_id:
        result = task_table.select(task_id == task_table.c.id).execute()
    else:
        result = task_table.select().execute()

    tasks = []
    for row in result:
        tasks.append({ 'id': row[0], 'title': row[1], 'isDone': row[2] })
        print tasks[-1]

    return tasks


def db_insert_task(title, dbm):
    meta = dbm.get_db_metadata('board')
    task_table = Table('tasks', meta, autoload=True)

    result = task_table.insert().execute(title=title, isDone=0)
    newId = result.inserted_primary_key[0]
    print 'INSERT new id: %d' % newId

    return newId


def db_update_task(task, dbm):
    meta = dbm.get_db_metadata('board')
    task_table = Table('tasks', meta, autoload=True)

    result = task_table.update(task['id'] == task_table.c.id).execute(isDone=task['isDone'], title=task['title'])
    print 'UPDATE matched: %d' % result.rowcount


def db_delete_task(task, dbm):
    meta = dbm.get_db_metadata('board')
    task_table = Table('tasks', meta, autoload=True)

    result = task_table.delete(task['id'] == task_table.c.id).execute()
    print 'DELETE matched: %d' % result.rowcount
