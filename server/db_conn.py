from server.sql_strings import SQLs
from server.db_schema import DbSchema, TableSchema
from server.util import *

import sqlite3
import csv
from sqlite3.dbapi2 import Connection, Cursor

# Sqlite tutorial: https://docs.python.org/3/library/sqlite3.html


class DatabaseConnection:
    connection: Connection
    cursor: Cursor

    def __init__(self):
        self.connection = sqlite3.connect('server/sqlite/database.db',
                                          check_same_thread=False)
        self.cursor = self.connection.cursor()

        tables = self.cursor.execute(SQLs.list_tables).fetchall()
        for table in DbSchema.tables:
            if (table.name, ) not in tables:
                self.__create_table(table)
            if self.cursor.execute(SQLs.count.format(
                    table.name)).fetchone() == (0, ):
                self.__insert_initial_data(table)

    def __create_table(self, table: TableSchema):
        items = table.schema.items()
        columns = ""
        for index, (key, value) in enumerate(items):
            if index == 0:
                columns += SQLs.create_table__row_primary.format(key)
            else:
                columns += SQLs.create_table__row.format(key, value)

            if index < len(items) - 1:
                columns += ','

        sql = SQLs.create_table.format(table.name, columns)
        self.cursor.execute(sql)

    def __insert_initial_data(self, table: TableSchema):
        # Read test data
        with open(table.initial_data_path, 'r') as testDataFile:
            data = list(csv.reader(testDataFile))

        # insert into db
        sql_columns = ""
        for index, key in enumerate(data[0]):
            sql_columns += key
            if index < len(data[0]) - 1:
                sql_columns += ","

        sql_rows = ""
        for obj_index, obj in enumerate(data):
            if obj_index == 0:
                continue

            sql_row = ""
            for index, value in enumerate(obj):
                int_value = try_parse_int(value)
                if int_value != None:
                    sql_row += value
                else:
                    sql_row += '"{}"'.format(value)

                if index < len(obj) - 1:
                    sql_row += ","

            sql_rows += SQLs.insert_row.format(sql_row)
            if obj_index < len(data) - 1:
                sql_rows += ","

        sql = SQLs.insert.format(table.name, sql_columns, sql_rows)
        self.cursor.execute(sql)
        self.connection.commit()

    def get_tasks(self, offset: int, limit: int):
        # yapf: disable
        tasks = self.cursor.execute(
            SQLs.select.format(DbSchema.table_tasks.name) +
            SQLs.order_by.format('state DESC, dueByDate ASC') +
            SQLs.limit.format(str(limit)) +
            SQLs.offset.format(str(offset))
        ).fetchall()
        # yapf: enable

        more = len(tasks) > limit + offset
        return tasks, more
