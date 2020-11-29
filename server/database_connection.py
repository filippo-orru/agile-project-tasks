from server.sql_strings import SQLs
from server.util import *

import sqlite3
from sqlite3.dbapi2 import Connection, Cursor

# Sqlite tutorial: https://docs.python.org/3/library/sqlite3.html


class DatabaseConnection:
    connection: Connection
    cursor: Cursor

    def __init__(self):
        self.connection = sqlite3.connect('server/sqlite/database.db',
                                          check_same_thread=False)
        self.cursor = self.connection.cursor()

    def execute_sql(self, sql):
        val = self.cursor.execute(sql)
        self.connection.commit()
        return val
