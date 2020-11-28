from sqlite3.dbapi2 import Cursor
from server.sql_strings import SQLs
from abc import ABC, abstractmethod


class CollectionItem(ABC):
    @abstractmethod
    def toSql():
        pass


class Task(CollectionItem):
    id: int
    name: str
    description: str
    state: str
    assignee: str
    createdDate: str
    createdBy: str
    dueByDate: str

    schema: dict = {
        'id': 'INTEGER',
        'name': 'STRING',
        'description': 'STRING',
        'state': 'STRING',
        'assignee': 'STRING',
        'createdDate': 'STRING',
        'createdBy': 'STRING',
        'dueByDate': 'STRING',
    }

    def __init__(self, id, name, description, state, assignee, createdDate,
                 createdBy, dueByDate):
        self.id = id
        self.name = name
        self.description = description
        self.state = state
        self.assignee = assignee
        self.createdDate = createdDate
        self.createdBy = createdBy
        self.dueByDate = dueByDate

    def fromJson(json):
        return Task(json["id"], json["name"], json["description"],
                    json["state"], json["assignee"], json["createdDate"],
                    json["createdBy"], json["dueByDate"])

    def toSql(self):
        return SQLs.insert_row.format(
            "\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"".format(
                self.name,
                self.description,
                self.state,
                self.assignee,
                self.createdDate,
                self.createdBy,
                self.dueByDate,
            ))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "state": self.state,
            "assignee": self.assignee,
            "createdDate": self.createdDate,
            "createdBy": self.createdBy,
            "dueByDate": self.dueByDate
        }


class AbstractCollection(ABC):
    name: str
    initial_data_path: str
    schema: dict  # 'id' column is always used as primary key
    cursor: Cursor

    def __init__(self, name: str, initial_data_path: str, schema: dict,
                 cursor):
        self.name = name
        self.initial_data_path = initial_data_path
        self.schema = schema
        self.cursor = cursor

    def get(self, id: int) -> Task:
        sql = SQLs.select.format(self.name) + SQLs.where.format(
            "id = {}".format(id))
        return self.cursor.execute(sql).fetchone()

    def insert(self, item: CollectionItem) -> Task:
        sql = SQLs.insert.format(self.name, self.get_columns_sql(),
                                 item.toSql())
        self.cursor.execute(sql)
        return self.get(self.cursor.lastrowid)

    def get_columns_sql(self) -> str:
        columns = list(self.schema.keys())
        columns.pop(columns.index('id'))
        return str(columns)[1:-1].replace("'", '')


class Tasks(AbstractCollection):
    def __init__(self, cursor: Cursor):
        super().__init__('tasks', 'resources/test_data.csv', Task.schema,
                         cursor)

    def get_many(self, offset: int, limit: int):
        all_tasks_count = self.cursor.execute(SQLs.count.format(
            self.name)).fetchone()[0]

        # yapf: disable
        tasks = self.cursor.execute(
            SQLs.select.format(self.name) +
            SQLs.order_by.format('state DESC, dueByDate ASC') +
            SQLs.limit.format(str(limit)) +
            SQLs.offset.format(str(offset))
        ).fetchall()
        # yapf: enable

        more = all_tasks_count > limit + offset
        return tasks, more


class Collections:
    tasks: Tasks

    def __init__(self, cursor):
        self.tasks = Tasks(cursor)

    def all(self):
        return [self.tasks]