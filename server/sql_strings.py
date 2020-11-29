class SQLs:
    list_tables = """
    SELECT 
        name
    FROM 
        sqlite_master 
    WHERE 
        type ='table' AND 
        name NOT LIKE 'sqlite_%';
    """

    create_table = "CREATE TABLE IF NOT EXISTS {}({});"

    create_table__row_primary = "{} INTEGER PRIMARY KEY"

    create_table__row = "{} {} NOT NULL"

    select = "SELECT * FROM {} "

    where = "WHERE {} "

    order_by = "ORDER BY {} "

    limit = "LIMIT {} "

    offset = "OFFSET {} "

    insert = "INSERT INTO {} ({}) VALUES {}"

    insert_row = "({})"

    count = "SELECT COUNT(*) FROM {}"

    get_schema_version = 'SELECT version FROM schema WHERE name="{}"'

    drop = "DROP TABLE {}"

    insert_schema = 'INSERT INTO schema(name,version) VALUES("{0}","{1}") ON CONFLICT(name) DO UPDATE SET version={1};'