from server.sql_strings import SQLs
from server.abstract_collections import *


class Task(CollectionItem):
    name: str
    description: str
    state: str
    assignee: str
    createdDate: str
    createdBy: str
    dueByDate: str

    def __init__(self, id, name, description, state, assignee, createdDate,
                 createdBy, dueByDate):
        super().__init__(id)
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

    def toDict(self):
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


class Tasks(AbstractCollection):
    schema = Schema(version=2,
                    body={
                        'id': 'INTEGER',
                        'name': 'TEXT',
                        'description': 'TEXT',
                        'state': 'TEXT',
                        'assignee': 'TEXT',
                        'createdDate': 'TEXT',
                        'createdBy': 'TEXT',
                        'dueByDate': 'TEXT',
                    })

    def __init__(self, database_connection: DatabaseConnection):
        super().__init__('tasks', 'resources/test_data.csv', self.schema, Task,
                         database_connection)

    def get_many(self, offset: int, limit: int):
        all_tasks_count = self.database_connection.execute_sql(
            SQLs.count.format(self.name)).fetchone()[0]

        # yapf: disable
        tasks = self.database_connection.execute_sql(
            SQLs.select.format(self.name) +
            SQLs.order_by.format('state DESC, dueByDate ASC') +
            SQLs.limit.format(str(limit)) +
            SQLs.offset.format(str(offset))
        ).fetchall()
        # yapf: enable

        tasks = list(map(lambda tuple: Task(*tuple), tasks))
        more = all_tasks_count > limit + offset
        return tasks, more


class Collections:
    tasks: Tasks

    def __init__(self, database_connection: DatabaseConnection):
        self.tasks = Tasks(database_connection)

    def all(self):
        return [self.tasks]