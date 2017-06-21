import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import psycopg2
from psycopg2.extras import RealDictCursor

from settings import DATABASES


class Database(object):

    def __init__(self):
        self.connection = self.__connection()

    def __connection(self, dbname='default'):
        credentials = DATABASES[dbname]
        conn_string = '''host={host} dbname={db_name} user={user} password={password} port={port}'''.format(
            host=credentials['HOST'],
            db_name=credentials['NAME'],
            user=credentials['USER'],
            password=credentials['PASSWORD'],
            port=credentials['PORT'])
        conn = psycopg2.connect(conn_string)
        return conn

    def execute_query(self, query):
        cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        self.connection.commit()
        return cursor

    def close_connection(self):
        self.connection.close()
