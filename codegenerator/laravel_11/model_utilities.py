from mysql.connector.connection import MySQLConnection
from typing import List, Dict, Any
import inflect

p = inflect.engine()


def has_many(connection: MySQLConnection, table_name: str) -> List[str]:
    cursor = connection.cursor()

    singular = p.singular_noun(table_name)

    # Query for tables based on naming convention
    query1 = """
    SELECT DISTINCT TABLE_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE (COLUMN_NAME = %s OR COLUMN_NAME LIKE %s)
    AND TABLE_NAME != %s
    AND TABLE_NAME NOT LIKE '%%\_%%'
    """

    cursor.execute(query1, (f"{singular}_id", f"%_{singular}_id", table_name))
    results = set(row[0] for row in cursor.fetchall())

    # Query for tables explicitly referencing this table through foreign keys
    query2 = """
    SELECT DISTINCT TABLE_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE REFERENCED_TABLE_NAME = %s
    AND TABLE_NAME != %s
    AND TABLE_NAME NOT LIKE '%%\_%%'
    """

    cursor.execute(query2, (table_name, table_name))
    fk_results = set(row[0] for row in cursor.fetchall())

    # Combine results
    results.update(fk_results)

    cursor.close()
    return list(results)


def belongs_to(connection: MySQLConnection, table_name: str) -> List[str]:
    cursor = connection.cursor()

    # Query for tables based on naming convention
    query1 = """
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = %s
    AND (COLUMN_NAME LIKE '%%\_id' AND COLUMN_NAME != 'id')
    """

    cursor.execute(query1, (table_name,))

    results = set()
    for row in cursor.fetchall():
        column_name = row[0]
        if '_' in column_name:
            referenced_table = p.plural(column_name.split('_')[-2])
        else:
            referenced_table = p.plural(column_name[:-3])
        results.add(referenced_table)

    # Query for tables explicitly referenced by this table through foreign keys
    query2 = """
    SELECT DISTINCT REFERENCED_TABLE_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_NAME = %s
    AND REFERENCED_TABLE_NAME IS NOT NULL
    """

    cursor.execute(query2, (table_name,))
    fk_results = set(row[0] for row in cursor.fetchall())

    # Combine results
    results.update(fk_results)

    cursor.close()
    return list(results)


def get_pivot_tables(connection: MySQLConnection, table_name: str) -> List[str]:
    cursor = connection.cursor()

    query = """
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME LIKE %s OR TABLE_NAME LIKE %s
    """

    cursor.execute(query, (f"{table_name}_%", f"%_{table_name}"))

    results = [row[0] for row in cursor.fetchall()]

    cursor.close()
    return results


def has_many_through(connection: MySQLConnection, table_name: str, excluded_columns: List[str]) -> List[Dict[str, Any]]:
    cursor = connection.cursor()

    pivot_tables = get_pivot_tables(connection, table_name)

    results = []
    singular = p.singular_noun(table_name)

    for pivot_table in pivot_tables:
        query = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = %s
        """
        cursor.execute(query, (pivot_table,))
        columns = [row[0] for row in cursor.fetchall()]

        other_columns = [col for col in columns
                         if col not in excluded_columns
                         and col != f"{singular}_id"
                         and not (col.endswith('_id') and col.split('_')[-2] == singular)]

        if other_columns:
            other_table_parts = pivot_table.replace(table_name, '').replace('_', '').strip()
            if not other_table_parts:
                other_table_parts = pivot_table.replace(f"{table_name}_", '').replace(f"_{table_name}", '')
            other_table = p.plural(other_table_parts)

            results.append({
                "table": other_table,
                "columns": other_columns
            })

    cursor.close()
    return results
#
# # Example usage:
# if __name__ == "__main__":
#     # Replace with your actual database connection details
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="yourusername",
#         password="yourpassword",
#         database="yourdatabase"
#     )
#
#     try:
#         print(hasMany(connection, "users"))
#         print(belongsTo(connection, "users"))
#         print(get_pivot_tables(connection, "users"))
#         print(hasManyThrough(connection, "users", ["created_at", "updated_at"]))
#     finally:
#         connection.close()
