from codegenerator.laravel_11 import utilities
from mysql.connector.connection import MySQLConnection


def get_first_text_like_column_from_table_name(connection: MySQLConnection, table_name: str):
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
    cursor.close()

    if result:
        return result[0]
    else:
        return "id"


def react_index_table_data_cells(columns, ignore_columns, table_name, belongs_to_list, connection):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] == 'id':
            continue
        col_name = column['COLUMN_NAME']
        if utilities.remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
            table_nm = utilities.get_table_name_from_fk_column_name(column['COLUMN_NAME'], belongs_to_list, ignore_columns)
            col_nm = get_first_text_like_column_from_table_name(connection, table_nm)
            col_name = f"{table_nm}.{col_nm}"
        return_string += " " * 20 + f"""<TableCell>
                      {{ {table_name}.{col_name} }}
                    </TableCell>\n"""
    return return_string


def get_react_index_table_headings(columns, ignore_columns, belongs_to_list):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] == 'id':
            continue
        col_name = column['COLUMN_NAME']
        if utilities.remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
            col_name = utilities.get_as_name_for_fk_col(column['COLUMN_NAME'], belongs_to_list)
        return_string += " " * 20 + f"""<TableHeading
                      name="{col_name}"
                      sort_field={{mergedQueryParams.sort_field}}
                      sort_direction={{mergedQueryParams.sort_direction}}
                      sortChanged={{sortChanged}}
                    >
                      {utilities.any_case_to_title(utilities.remove_id_suffix(column['COLUMN_NAME']))}
                    </TableHeading>\n"""
    return return_string


def get_react_index_table_search_headings(columns, ignore_columns, belongs_to_list):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] == 'id':
            continue
        col_name = column['COLUMN_NAME']
        tab_name = column['COLUMN_NAME']
        if utilities.remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
            col_name = utilities.get_as_name_for_fk_col(column['COLUMN_NAME'], belongs_to_list)
            tab_name = utilities.get_table_name_from_fk_column_name(column['COLUMN_NAME'], belongs_to_list, ignore_columns)
        return_string += " " * 20 + f"""<TableCell>
                                            <TextField
                                                fullWidth
                                                defaultValue={{
                                                    queryParams?.{col_name} ?? ""
                                                }}
                                                placeholder="{utilities.any_case_to_title(utilities.singular(tab_name))}"
                                                onBlur={{(e) =>
                                                    searchFieldChanged(
                                                        "{col_name}",
                                                        e.target.value
                                                    )
                                                }}
                                                onKeyPress={{(e) =>
                                                    onKeyPress("{col_name}", e)
                                                }}
                                            />
                                        </TableCell>\n"""
    return return_string
