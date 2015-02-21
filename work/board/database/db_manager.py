import logging
import sqlalchemy

logger = logging.getLogger("db_manager")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


# http://docs.sqlalchemy.org/en/rel_0_9/core/tutorial.html


class db_manager:
    def __init__(self):
        self._engines = {}
        self._metadata = {}

    def setup_db(self, db_name, db_host, db_port, db_user, db_pass):
        self._engines[db_name] = self.__create_engine(db_name, db_host, db_port, db_user, db_pass)
        self._metadata[db_name] = sqlalchemy.MetaData(bind=self._engines[db_name])

    def get_db_engine(self, db_name):
        return self._engines[db_name]

    def get_db_metadata(self, db_name):
        return self._metadata[db_name]

    def __create_engine(self, db_name, db_host='localhost', db_port=3306, db_user='', db_pass=''):
        db_address = db_host + ":" + str(db_port)
        url = "mysql://%s:%s@%s/%s" % (db_user, db_pass, db_address, db_name)

        return sqlalchemy.create_engine(url, strategy='threadlocal' )
