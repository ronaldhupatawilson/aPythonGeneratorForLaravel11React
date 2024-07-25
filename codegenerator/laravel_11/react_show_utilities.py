from codegenerator.laravel_11 import utilities
from codegenerator.laravel_11 import model_utilities


def get_typescript_type_from_column_type(type):
    if type in ['int', 'bigint', 'mediumint', 'smallint', 'decimal', 'double', 'float', 'real']:
        return 'number'
    if type in ['char', 'varchar', 'text', 'smalltext', 'mediumtext', 'largetext', 'datetime', 'time', 'timestamp']:
        return 'string'
    if type in ['date']:
        return 'string'
    if type == 'tinyint':
        return 'bool'
    return False



def get_prop_val_from_column_type(type):
    if type in ['char', 'varchar', 'text', 'smalltext', 'mediumtext', 'largetext', 'datetime', 'time', 'timestamp']:
        return '""'
    return 'null'


def get_formdata_interface(columns, ignore_columns):
    ret_string = ""
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        ret_string += " " * 4 + f"""{column['COLUMN_NAME']}: {get_typescript_type_from_column_type(column['DATA_TYPE'])} | null;\n"""
    return ret_string


def get_props(columns, ignore_columns):
    ret_string = ""
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        ret_string += " " * 8 + f"""{column['COLUMN_NAME']}: {get_prop_val_from_column_type(column['DATA_TYPE'])},\n"""
    return ret_string


def get_display_fields(columns, ignore_columns, belongs_to_list, connection):
    ret_string = ""
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns or column['COLUMN_NAME'] == 'id':
            continue
        if column['COLUMN_NAME'].split('/')[-1].lower() == 'path':
            ret_string += f"""
                      <div className="flex justify-between">
                        <div>
                            {utilities.any_case_to_title({column['COLUMN_NAME']})}
                        </div>
                        <div>
                        Some media goes here - shows visibly if image or video - <a href="{{data.{column['COLUMN_NAME']}}}">{{data.{column['COLUMN_NAME']}}}</
                        </div>
                      </div>\n"""
        else:
            if utilities.remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
                ret_string += f"""                        <div className="flex justify-between mb-4">
                          <div>{utilities.any_case_to_title(utilities.remove_id_suffix(column['COLUMN_NAME']))}</div>
                          <div>{{ data.{model_utilities.get_first_text_like_column_from_table_name(connection, utilities.get_table_name_from_fk_column_name(column['COLUMN_NAME'], belongs_to_list, ignore_columns))} }}</div>
                        </div>\n"""
            else:
                ret_string += f"""<div className="flex justify-between mb-4"><div>{column['COLUMN_NAME']}</div><div>{{data.{column['COLUMN_NAME']}}}</div></div>\n"""

    return ret_string


def get_own_interface(columns, ignore_columns, belongs_to_list, ln):
    ret_string = f"""\ninterface {utilities.any_case_to_pascal_case(utilities.singular(ln.tn))} {{
  \n"""
    ret_string += utilities.get_typescript_interface_fields(columns, ignore_columns)
    for fk in belongs_to_list:
        if fk['column_name'] in ignore_columns:
            continue
        ret_string += f"""  {(fk['table_name']+fk['view_column']).lower()}: string
  }}\n"""
    ret_string += """ }} """
    return ret_string


def get_props_interface(ln):
    ret_string = f"""interface Props {{
    auth: Auth;
    {ln.lcs} : {ln.lcs};
  }}"""
    return ret_string


def get_props_interfaces_as_csl(ignore_columns, belongs_to_list):
    ret_string = """auth  """
    for fk in belongs_to_list:
        if fk['column_name'] in ignore_columns:
            continue
        if utilities.remove_id_suffix(fk['column_name']) != fk['column_name']:
            ret_string += f""", {fk['table_name']}"""
    return ret_string