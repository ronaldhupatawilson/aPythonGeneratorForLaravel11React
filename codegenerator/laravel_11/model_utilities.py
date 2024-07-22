from mysql.connector.connection import MySQLConnection
from typing import List, Dict, Any
from codegenerator.laravel_11 import utilities
from pprint import pprint


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
    results = set((row[0], row[1]) for row in cursor.fetchall())

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
    fk_results = set((row[0], row[1]) for row in cursor.fetchall())

    # Combine results
    results.update(fk_results)

    cursor.close()
    return [{"table_name": table, "column_name": column} for table, column in results]


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
        results.append({"table_name": referenced_table, "column_name": column_name})

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
    fk_results = [{"table_name": row['TABLE_NAME'], "column_name": row['COLUMN_NAME']} for row in cursor.fetchall()]

    # Combine results
    results.extend(fk_results)

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for item in results:
        item_tuple = tuple(item.items())
        if item_tuple not in seen:
            seen.add(item_tuple)
            unique_results.append(item)

    cursor.close()
    return unique_results

# def belongs_to(connection: MySQLConnection, table_name: str) -> List[str]:
#     cursor = connection.cursor()
#
#     # Query for tables based on naming convention
#     query1 = """
#     SELECT DISTINCT COLUMNS.TABLE_NAME as TABLE_NAME, COLUMN_NAME
#     FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
#     WHERE COLUMNS.TABLE_NAME = %s
#     AND (COLUMN_NAME LIKE '%%\\_id' AND COLUMN_NAME != 'id')
#     AND COLUMNS.TABLE_SCHEMA = %s
#     AND TABLES.TABLE_TYPE = 'BASE TABLE'
#     """
#
#     cursor.execute(query1, (table_name, connection.database))
#
#     results = set()
#     for row in cursor.fetchall():
#         column_name = row[0]
#         if '_' in column_name:
#             referenced_table = utilities.plural(column_name.split('_')[-2])
#         else:
#             referenced_table = utilities.plural(column_name[:-3])
#         results.add(referenced_table)
#
#     # Query for tables explicitly referenced by this table through foreign keys
#     query2 = """
#     SELECT DISTINCT KEY_COLUMN_USAGE.REFERENCED_TABLE_NAME AS TABLE_NAME, COLUMN_NAME
#     FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE JOIN INFORMATION_SCHEMA.TABLES ON (KEY_COLUMN_USAGE.TABLE_NAME = TABLES.TABLE_NAME AND KEY_COLUMN_USAGE.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
#     WHERE KEY_COLUMN_USAGE.TABLE_NAME = %s
#     AND KEY_COLUMN_USAGE.REFERENCED_TABLE_NAME IS NOT NULL
#     AND KEY_COLUMN_USAGE.TABLE_SCHEMA = %s
#     AND TABLES.TABLE_TYPE = 'BASE TABLE'
#     """
#
#     cursor.execute(query2, (table_name, connection.database))
#     fk_results = set(row[0] for row in cursor.fetchall())
#
#     # Combine results
#     results.update(fk_results)
#
#     cursor.close()
#     return list(results)


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

        other_table_name_singular = utilities.singular(other_table_name)

        other_columns = [col for col in columns
                         if col not in excluded_columns
                         and col != f"{singular}_id"
                         and col != f"{other_table_name_singular}_id"]

        results.append({
                "table": other_table_name,
                "columns": other_columns
            })

    cursor.close()
    return results
