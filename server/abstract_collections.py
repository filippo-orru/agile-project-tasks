from server.sql_strings import SQLs
from server.database_connection import DatabaseConnection
from abc import ABC, abstractmethod

import csv


class CollectionItem(ABC):
    @abstractmethod
    def toSql():
        pass


class AbstractCollection(ABC):
    name: str
    initial_data_path: str
    schema: dict  # 'id' column is always used as primary key
    database_connection: DatabaseConnection

    def __init__(self, name: str, initial_data_path: str, schema: dict,
                 database_connection: DatabaseConnection):
        self.name = name
        self.initial_data_path = initial_data_path
        self.schema = schema
        self.database_connection = database_connection

        db_tables = database_connection.execute_sql(
            SQLs.list_tables).fetchall()

        if (self.name, ) not in db_tables:
            self.__create_table()

        if self.database_connection.execute_sql(SQLs.count.format(
                self.name)).fetchone() == (0, ):
            self.__insert_initial_data()

    def __create_table(self):
        items = self.schema.items()
        columns_sql = ""
        for index, (key, value) in enumerate(items):
            if index == 0:
                columns_sql += SQLs.create_table__row_primary.format(key)
            else:
                columns_sql += SQLs.create_table__row.format(key, value)

            if index < len(items) - 1:
                columns_sql += ','

        sql = SQLs.create_table.format(self.name, columns_sql)
        self.database_connection.execute_sql(sql)

    def __insert_initial_data(self):
        # Read test data
        with open(self.initial_data_path, 'r') as testDataFile:
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
            self.name, self.get_columns_sql(include_primary_key=True),
            sql_rows)
        self.database_connection.execute_sql(sql)

    def get(self, id: int) -> CollectionItem:
        sql = SQLs.select.format(self.name) + SQLs.where.format(
            "id = {}".format(id))
        return self.database_connection.execute_sql(sql).fetchone()

    def insert(self, item: CollectionItem) -> CollectionItem:
        sql = SQLs.insert.format(self.name, self.get_columns_sql(),
                                 item.toSql())
        self.execute_sql(sql)
        return self.get(self.cursor.lastrowid)

    def get_columns_sql(self, include_primary_key: bool = False) -> str:
        columns = list(self.schema.keys())
        if not include_primary_key: columns.pop(columns.index('id'))
        return str(columns)[1:-1].replace("'", '')
