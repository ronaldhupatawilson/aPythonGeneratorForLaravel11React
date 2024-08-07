from mysql.connector.connection import MySQLConnection
from typing import List, Dict, Any
from codegenerator.laravel_11 import utilities
from pprint import pprint


def get_first_text_like_column_from_table_name(connection: MySQLConnection, table_name: str) -> List[str]:
    cursor = connection.cursor()

    query = """
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
    WHERE COLUMNS.TABLE_NAME = %s
    AND COLUMNS.TABLE_SCHEMA = %s
    AND TABLES.TABLE_TYPE = 'BASE TABLE'
    AND COLUMNS.DATA_TYPE IN ('char','varchar','smalltext','mediumtext','text','largetext')
    ORDER BY COLUMNS.ORDINAL_POSITION
    LIMIT 0,1
    """

    cursor.execute(query, (table_name, connection.database))

    result = cursor.fetchone()

    if result:
        cursor.close()
        return result[0]
    else:
        query = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
        WHERE COLUMNS.TABLE_NAME = %s
        AND COLUMNS.TABLE_SCHEMA = %s
        AND TABLES.TABLE_TYPE = 'BASE TABLE'
        AND COLUMNS.DATA_TYPE IN ('time','datetime','date','timestamp')
        ORDER BY COLUMNS.ORDINAL_POSITION
        LIMIT 0,1
        """

        cursor.execute(query, (table_name, connection.database))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return "id"


def has_many(connection: MySQLConnection, table_name: str) -> List[str]:
    cursor = connection.cursor()

    singular_table_name = utilities.singular(table_name)

    # Query for tables based on naming convention
    query1 = """
    SELECT DISTINCT COLUMNS.TABLE_NAME, COLUMNS.COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
    WHERE (COLUMN_NAME = %s OR COLUMN_NAME LIKE %s)
    AND COLUMNS.TABLE_NAME != %s
    AND COLUMNS.TABLE_NAME NOT LIKE '%%\\_%%'
    AND COLUMNS.TABLE_SCHEMA = %s
    AND TABLES.TABLE_TYPE = 'BASE TABLE'
    """

    cursor.execute(query1, (f"{singular_table_name}_id", f"%_{singular_table_name}_id", table_name, connection.database))
    results = set((row[0], row[1], get_first_text_like_column_from_table_name(connection, row[0])) for row in cursor.fetchall())

    # Query for tables explicitly referencing this table through foreign keys
    query2 = """
    SELECT DISTINCT KEY_COLUMN_USAGE.TABLE_NAME, KEY_COLUMN_USAGE.COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE JOIN INFORMATION_SCHEMA.TABLES ON (KEY_COLUMN_USAGE.TABLE_NAME = TABLES.TABLE_NAME AND KEY_COLUMN_USAGE.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
    WHERE REFERENCED_TABLE_NAME = %s
    AND KEY_COLUMN_USAGE.TABLE_NAME != %s
    AND KEY_COLUMN_USAGE.TABLE_NAME NOT LIKE '%%\\_%%'
    AND KEY_COLUMN_USAGE.TABLE_SCHEMA = %s
    AND TABLES.TABLE_TYPE = 'BASE TABLE'
    """

    cursor.execute(query2, (table_name, table_name, connection.database))
    fk_results = set((row[0], row[1], get_first_text_like_column_from_table_name(connection, row[0])) for row in cursor.fetchall())

    # Combine results
    results.update(fk_results)

    cursor.close()
    return [{"table_name": table, "column_name": column, 'view_column': view_col} for table, column, view_col in results]


def belongs_to(connection: MySQLConnection, table_name: str) -> List[Dict[str, str]]:
    cursor = connection.cursor(dictionary=True)

    # Query for tables based on naming convention
    query1 = """
    SELECT DISTINCT COLUMNS.TABLE_NAME as TABLE_NAME, COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
    WHERE COLUMNS.TABLE_NAME = %s
    AND (COLUMN_NAME LIKE '%%\\_id' AND COLUMN_NAME != 'id')
    AND COLUMNS.TABLE_SCHEMA = %s
    AND TABLES.TABLE_TYPE = 'BASE TABLE'
    """

    cursor.execute(query1, (table_name, connection.database))

    results = []
    for row in cursor.fetchall():
        column_name = row['COLUMN_NAME']
        if '_' in column_name:
            referenced_table = utilities.plural(column_name.split('_')[-2])
        else:
            referenced_table = utilities.plural(column_name[:-3])
        view_column = get_first_text_like_column_from_table_name(connection, referenced_table)
        results.append({"table_name": referenced_table, "column_name": column_name, "view_column": view_column})

    # Query for tables explicitly referenced by this table through foreign keys
    query2 = """
    SELECT DISTINCT KEY_COLUMN_USAGE.REFERENCED_TABLE_NAME AS TABLE_NAME, COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE JOIN INFORMATION_SCHEMA.TABLES ON (KEY_COLUMN_USAGE.TABLE_NAME = TABLES.TABLE_NAME AND KEY_COLUMN_USAGE.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
    WHERE KEY_COLUMN_USAGE.TABLE_NAME = %s
    AND KEY_COLUMN_USAGE.REFERENCED_TABLE_NAME IS NOT NULL
    AND KEY_COLUMN_USAGE.TABLE_SCHEMA = %s
    AND TABLES.TABLE_TYPE = 'BASE TABLE'
    """

    cursor.execute(query2, (table_name, connection.database))
    fk_results = [{"table_name": row['TABLE_NAME'], "column_name": row['COLUMN_NAME'], "view_column": get_first_text_like_column_from_table_name(connection, row['TABLE_NAME'])} for row in cursor.fetchall()]

    # Combine results
    results.extend(fk_results)

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for item in results:
        key = (item['table_name'], item['column_name'], item['view_column'])
        if key not in seen:
            seen.add(key)
            unique_results.append(item)

    cursor.close()
    return unique_results


def get_pivot_tables(connection: MySQLConnection, table_name: str) -> List[str]:
    cursor = connection.cursor()

    query = """
    SELECT DISTINCT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE ((TABLE_NAME LIKE %s )
    OR (TABLE_NAME LIKE %s ))
    AND TABLE_SCHEMA = %s
    AND TABLE_TYPE = 'BASE TABLE'
    """

    cursor.execute(query, (f"{table_name}\\_%", f"%\\_{table_name}", connection.database))

    results = [row[0] for row in cursor.fetchall()]

    cursor.close()
    return results


def has_many_through(connection: MySQLConnection, table_name: str, excluded_columns: List[str]) -> List[Dict[str, Any]]:
    cursor = connection.cursor()

    pivot_tables = get_pivot_tables(connection, table_name)

    results = []
    singular = utilities.singular(table_name)

    for pivot_table in pivot_tables:
        query = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
        WHERE COLUMNS.TABLE_NAME = %s
        AND COLUMNS.TABLE_SCHEMA = %s
        AND TABLES.TABLE_TYPE = 'BASE TABLE'
        """
        cursor.execute(query, (pivot_table, connection.database))
        columns = [row[0] for row in cursor.fetchall()]

        other_table_name = pivot_table.replace(table_name, '').replace('_', '').strip()
        view_column = get_first_text_like_column_from_table_name(connection, other_table_name)

        other_table_name_singular = utilities.singular(other_table_name)

        other_columns = [col for col in columns
                         if col not in excluded_columns
                         and col != f"{singular}_id"
                         and col != f"{other_table_name_singular}_id"]

        results.append({
                "table_name": other_table_name,
                "columns": other_columns,
                "view_column": view_column
            })

    cursor.close()
    return results
