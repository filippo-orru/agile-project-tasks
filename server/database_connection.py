from server.sql_strings import SQLs
from server.collections import Collections, AbstractCollection, Task
from server.util import *

import sqlite3
import csv
from sqlite3.dbapi2 import Connection, Cursor

# Sqlite tutorial: https://docs.python.org/3/library/sqlite3.html


class DatabaseConnection:
    connection: Connection
    cursor: Cursor
    collections: Collections

    def __init__(self):
        self.connection = sqlite3.connect('server/sqlite/database.db',
                                          check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.collections = Collections(self.cursor)

        db_tables = self.__execute_sql(SQLs.list_tables).fetchall()
        for table in self.collections.all():
            if (table.name, ) not in db_tables:
                self.__create_table(table)

            if self.__execute_sql(SQLs.count.format(
                    table.name)).fetchone() == (0, ):
                self.__insert_initial_data(table)

    def __execute_sql(self, sql):
        val = self.cursor.execute(sql)
        self.connection.commit()
        return val

    def __create_table(self, table: AbstractCollection):
        items = table.schema.items()
        columns_sql = ""
        for index, (key, value) in enumerate(items):
            if index == 0:
                columns_sql += SQLs.create_table__row_primary.format(key)
            else:
                columns_sql += SQLs.create_table__row.format(key, value)

            if index < len(items) - 1:
                columns_sql += ','

        sql = SQLs.create_table.format(table.name, columns_sql)
        self.__execute_sql(sql)

    def __insert_initial_data(self, table: AbstractCollection):
        # Read test data
        with open(table.initial_data_path, 'r') as testDataFile:
            data = list(csv.reader(testDataFile))

        # Insert into db
        sql_rows = ""
        for obj_index, obj in enumerate(data):
            if obj_index == 0:
                continue

            sql_row = ""
            for index, value in enumerate(obj):
                sql_row += '"{}"'.format(value)

                if index < len(obj) - 1:
                    sql_row += ","

            sql_rows += SQLs.insert_row.format(sql_row)
            if obj_index < len(data) - 1:
                sql_rows += ","

        sql = SQLs.insert.format(
            table.name, table.get_columns_sql(include_primary_key=True),
            sql_rows)
        self.__execute_sql(sql)
