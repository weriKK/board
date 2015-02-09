from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table


engine = create_engine('mysql+pymysql://board:board@localhost/board', strategy='threadlocal')
metadata = MetaData(bind=engine)

tasksdb = Table('tasks', metadata, autoload=True)

result = tasksdb.insert().execute(title='NEW1', isDone=0)
newId = result.inserted_primary_key[0]
print 'INSERT new id: %d' % newId

result = tasksdb.update(newId == tasksdb.c.id).execute(title='HELLO UPDATE2')
print 'UPDATE matched: %d' % result.rowcount

result = tasksdb.delete(newId == tasksdb.c.id).execute()
print 'DELETE matched: %d' % result.rowcount

result = tasksdb.select().execute()
tasks = []
for row in result:
    tasks.append({ 'id': row[0], 'title': row[1], 'isDone': row[2] })
    print tasks[-1]

def db_save_task(task):
    result = tasksdb.update(task['id'] == tasksdb.c.id).execute(isDone=task['isDone'], title=task['title'])
    print 'UPDATE matched: %d' % result.rowcount


# update
# insert (get new id)
# delete
# logging


# tasks = [
#     {'id': 1,  'isDone': 1, 'title': 'First task to do'},
#     {'id': 2,  'isDone': 0, 'title': 'Second task to do'},
#     {'id': 3,  'isDone': 0, 'title': 'Third task to do'},
#     {'id': 4,  'isDone': 0, 'title': 'Fourth task to do'},
#     {'id': 5,  'isDone': 1, 'title': 'Fifth task to do'},
#     {'id': 6,  'isDone': 0, 'title': 'Sixth task to do'},
#     {'id': 7,  'isDone': 0, 'title': 'Seventh task to do'},
#     {'id': 8,  'isDone': 1, 'title': 'Eighth task to do'},
#     {'id': 9,  'isDone': 0, 'title': 'Nineth task to do'},
#     {'id': 10, 'isDone': 0, 'title': 'Tenth task to do'}
# ]
