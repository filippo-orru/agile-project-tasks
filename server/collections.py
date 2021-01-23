from datetime import date, datetime, timedelta
from sqlite3.dbapi2 import Date

from werkzeug.utils import escape
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

    def escape(string):
        '''
        Escapes potentially dangerous characters
        '''
        saveString = ""

        for x in string:
            if not (x.isalnum() or x.isspace()):
                saveString += "\\"
            saveString += x

        return saveString

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
        createdDate = date.today().strftime("%Y%m%d")
        return Task(0, escape(json["name"]), escape(json["description"]),
                    "Todo", escape(json["assignee"]), createdDate,
                    escape(json["createdBy"]), escape(json["dueByDate"]))

    def validate(self):
        '''
        Returns 'success' when a Task is valid.
        Otherwise returns an error message
        '''
        response = list()
        success = True
        if (self.name == ""):
            response.append("nameEmpty")
            success = False
        elif (len(self.name) > 25):
            response.append("nameTooLong")
            success = False
        if (self.dueByDate == ""):
            response.append("dueByDateEmpty")
            success = False
        elif (self.dueByDate < self.createdDate):
            response.append("dueByDateInPast")
            success = False
        else:
            try:
                datetime.strptime(self.dueByDate, '%Y%m%d')
            except ValueError:
                response.append("dueByDateInvalid")
                success = False

        if (self.createdBy == ""):
            response.append("createdByEmpty")
            success = False
        elif (len(self.createdBy) > 25):
            response.append("createdByTooLong")
            success = False
        if (self.assignee == ""):
            response.append("assigneeEmpty")
            success = False
        elif (len(self.assignee) > 25):
            response.append("assigneeTooLong")
            success = False
        if (self.description == ""):
            response.append("descriptionEmpty")
            success = False
        elif (len(self.description) > 40):
            response.append("descriptionTooLong")
            success = False
        # Success
        if success is True:
            response.append("success")

        return response

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

        sql = (SQLs.select.format(self.name) +
               SQLs.order_by.format('state DESC, dueByDate ASC'))

        if limit != -1:
            sql += SQLs.limit.format(str(limit))
            sql += SQLs.offset.format(str(offset))

        tasks = self.database_connection.execute_sql(sql).fetchall()

    def get_many(self, offset: int, limit: int, searchFilter: str):
        '''
        Set limit to -1 to get all tasks
        '''
        searchFilter = escape(searchFilter)
        all_tasks_count = self.database_connection.execute_sql(
            SQLs.count.format('(' + SQLs.select.format(self.name) +
                              SQLs.where.format("assignee LIKE ?") + ')'),
            ('%' + searchFilter + '%', )).fetchone()[0]

        sql = SQLs.select.format(self.name)
        params = None

        if searchFilter != None and len(searchFilter) > 0:
            sql += SQLs.where.format("assignee LIKE ?")
            params = ('%' + searchFilter + '%', )

        sql += SQLs.order_by.format('state DESC, dueByDate ASC')
        if limit != -1:
            sql += SQLs.limit.format(str(limit))
            sql += SQLs.offset.format(str(offset))

        tasks = self.database_connection.execute_sql(sql, params).fetchall()

        tasks = list(map(lambda tuple: Task(*tuple), tasks))
        more = all_tasks_count > limit + offset
        return tasks, more


class Collections:
    tasks: Tasks

    def __init__(self, database_connection: DatabaseConnection):
        self.tasks = Tasks(database_connection)

    def all(self):
        return [self.tasks]