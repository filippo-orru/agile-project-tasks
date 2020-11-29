from sqlite3.dbapi2 import OperationalError
from server.sql_strings import SQLs
from server.database_connection import DatabaseConnection

from typing import Any, Callable
from abc import ABC, abstractmethod

import csv


class Schema:
    version: int  # if table has other version, it will be dropped and recreated
    body: dict

    def __init__(self, version: int, body: dict):
        self.version = version
        self.body = body


class CollectionItem(ABC):
    id: int  # primary key

    def __init__(self, id: int):
        self.id = id

    @abstractmethod
    def toSql():
        raise NotImplementedError


class AbstractCollection(ABC):
    name: str
    initial_data_path: str
    schema: Schema
    # A constructor that takes arguments and returns CollectionItem
    collection_item: Callable[[Any], CollectionItem]
    database_connection: DatabaseConnection

    def __init__(self, name: str, initial_data_path: str, schema: Schema,
                 collection_item: Callable[[Any], CollectionItem],
                 database_connection: DatabaseConnection):
        self.name = name
        self.initial_data_path = initial_data_path
        self.schema = schema
        self.database_connection = database_connection
        self.collection_item = collection_item

        self.__check_tables()

    def __check_tables(self):
        db_tables = self.database_connection.execute_sql(
            SQLs.list_tables).fetchall()

        if (self.name, ) not in db_tables:
            self.__create_table()
        else:
            # Table exists. Check version
            try:
                existing_schema_version = self.database_connection.execute_sql(
                    SQLs.get_schema_version.format(self.name)).fetchone()[0]

                if existing_schema_version == None or existing_schema_version != self.schema.version:
                    self.__drop()
                    self.__create_table()
            except OperationalError:  # The schema table doesn't exist
                self.__drop()
                self.__create_table()

        if self.database_connection.execute_sql(SQLs.count.format(
                self.name)).fetchone()[0] == 0:
            self.__insert_initial_data()

    def __drop(self):
        self.database_connection.execute_sql(SQLs.drop.format(self.name))

    def __create_table(self):
        items = self.schema.body.items()
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

        self.__update_schema()

    def __update_schema(self):
        self.database_connection.execute_sql(
            SQLs.create_table.format(
                "schema", "name TEXT PRIMARY KEY, version INTEGER NOT NULL"))
        self.database_connection.execute_sql(
            SQLs.insert_schema.format(self.name, self.schema.version))

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
        task_tuple = self.database_connection.execute_sql(sql).fetchone()

        if task_tuple == None:
            return None
        else:
            return self.collection_item(*task_tuple)

    def insert(self, item: CollectionItem) -> CollectionItem:
        sql = SQLs.insert.format(self.name, self.get_columns_sql(),
                                 item.toSql())
        self.database_connection.execute_sql(sql)
        return self.get(self.database_connection.cursor.lastrowid)

    def get_columns_sql(self, include_primary_key: bool = False) -> str:
        columns = list(self.schema.body.keys())
        if not include_primary_key: columns.pop(columns.index('id'))
        return str(columns)[1:-1].replace("'", '')
