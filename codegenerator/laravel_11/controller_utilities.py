from mysql.connector.connection import MySQLConnection
from codegenerator.laravel_11 import utilities
from codegenerator.laravel_11 import laravel_object_and_file_names
from codegenerator.laravel_11 import column_info
from codegenerator.laravel_11 import model_utilities


def get_columns_from_table_name(table_name, connection):
    cursor = connection.cursor()
    cursor.execute(f"""SELECT COLUMNS.COLUMN_NAME, COLUMNS.ORDINAL_POSITION, COLUMNS.IS_NULLABLE, COLUMNS.DATA_TYPE, 
            COLUMNS.NUMERIC_PRECISION, COLUMNS.NUMERIC_SCALE, COLUMNS.CHARACTER_MAXIMUM_LENGTH, COLUMNS.COLUMN_KEY, COLUMNS.COLUMN_TYPE, 
            COLUMNS.EXTRA, COLUMNS.COLUMN_COMMENT, 
            COLUMNS.COLUMN_DEFAULT, KEY_COLUMN_USAGE.TABLE_NAME, KEY_COLUMN_USAGE.COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS LEFT JOIN
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE ON (  KEY_COLUMN_USAGE.TABLE_NAME = COLUMNS.TABLE_NAME 
            AND KEY_COLUMN_USAGE.TABLE_SCHEMA = COLUMNS.TABLE_SCHEMA 
            AND COLUMNS.COLUMN_NAME = KEY_COLUMN_USAGE.COLUMN_NAME  )
            WHERE COLUMNS.TABLE_SCHEMA = '{connection.database}' 
            AND COLUMNS.TABLE_NAME = '{table_name}' 
            ORDER BY COLUMNS.ORDINAL_POSITION""")
    columns = [
        {
            'COLUMN_NAME': row[0],
            'ORDINAL_POSITION': row[1],
            'IS_NULLABLE': row[2],
            'DATA_TYPE': row[3],
            'NUMERIC_PRECISION': row[4],
            'NUMERIC_SCALE': row[5],
            'CHARACTER_MAXIMUM_LENGTH': row[6],
            'COLUMN_KEY': row[7],
            'COLUMN_TYPE': row[8],
            'EXTRA': row[9],
            'COLUMN_COMMENT': row[10],
            'COLUMN_DEFAULT': row[11],
            'FK_TABLE':row[12],
            'FK_COLUMN':row[13]
        }
        for row in cursor.fetchall()
    ]
    return columns


def get_show_segment_for_belongs_to_many_table_named(table_name, ignore_columns, connection, where_string):
    ln = laravel_object_and_file_names.LaravelObjectAndFileNames(table_name, True, 'redis')
    columns = get_columns_from_table_name(table_name, connection)

    ci = column_info.ColumnInfo(columns, ignore_columns)
    ret_code = f"""
        ${table_name}_sortField = request("{table_name}_sort_field", 'created_at');
        ${table_name}_sortDirection = request("{table_name}_sort_direction", "desc");
        $query = {ln.model_class_name}::query();

 """
    belongs_to_list = model_utilities.belongs_to(connection, table_name)
    request_ref = []
    if len(belongs_to_list) > 0:
        select_ref = []
        is_first = True
        ret_code += f"""
        $query"""
        for fk_info in belongs_to_list:
            if not is_first:
                ret_code += ' ' * 12
            ret_code += f"""->leftJoin('{fk_info['table_name']}','{fk_info['table_name']}.id', '=', '{ln.tn}.{fk_info['column_name']}')\n"""
            sql_real_ref = f"""{fk_info['table_name']}.{fk_info['view_column']}"""
            as_name = f"""{utilities.any_case_to_camel_case(fk_info['table_name']+fk_info['view_column'])}"""
            select_ref_item = f"""'{sql_real_ref} as {as_name}'"""
            select_ref.append(select_ref_item)
            meta = {"actual_sql_ref": sql_real_ref, "as_name": as_name}
            request_ref.append(meta)
            is_first = False
        comma_separated_list = ", ".join(select_ref)
        ret_code += ' ' * 12  + f"""->select ('{ln.tn}.*', {comma_separated_list});"""
    ret_code += f"""

{ci.controller_index_where_statements}
"""
    if len(request_ref) > 0:
        for new_as_name in request_ref:
            ret_code +=  " " * 8 + f"""if (request('{new_as_name['as_name']}')) {{
                $query->where("{new_as_name['actual_sql_ref']}", "like", "%" . request("{new_as_name['as_name']}") ."%");
        }}\n\n"""
    ret_code += f"""
     {where_string}
        ${ln.lctn} = $query->orderBy(${table_name}_sortField, ${table_name}_sortDirection)
            ->paginate(20)
            ->onEachSide(1);
    """
    return ret_code
