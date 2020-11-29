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

    create_table = "CREATE TABLE {}({});"

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