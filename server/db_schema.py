class TableSchema:
    name: str
    initial_data_path: str
    schema: dict  # first column is used as primary key

    def __init__(self, name: str, initial_data_path: str, schema: dict):
        self.name = name
        self.initial_data_path = initial_data_path
        self.schema = schema


class DbSchema:
    table_tasks = TableSchema(
        'tasks', 'resources/test_data.csv', {
            'id': 'INTEGER',
            'name': 'STRING',
            'description': 'STRING',
            'state': 'STRING',
            'assignee': 'STRING',
            'createdDate': 'STRING',
            'createdBy': 'STRING',
            'dueByDate': 'STRING',
        })

    tables: list = [table_tasks]
