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
        or_null = " | null "
        if column['DATA_TYPE'] in ['char', 'varchar', 'text', 'smalltext', 'mediumtext', 'largetext', 'datetime', 'time', 'timestamp']:
            or_null = ""
        ret_string += " " * 4 + f"""{column['COLUMN_NAME']}: {get_typescript_type_from_column_type(column['DATA_TYPE'])}{or_null};\n"""
    return ret_string


def get_props(columns, ignore_columns):
    ret_string = ""
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        ret_string += " " * 8 + f"""{column['COLUMN_NAME']}: {get_prop_val_from_column_type(column['DATA_TYPE'])},\n"""
    return ret_string


def get_create_form_fields(columns, ignore_columns, belongs_to_list, connection):
    ret_string = ""
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns or column['COLUMN_NAME'] == 'id':
            continue
        target_value = """e.target.value"""
        if column['DATA_TYPE'] in ['bigint', 'int', 'tinyint', 'decimal', 'double', 'smallint', 'float']:
            target_value = """parseInt( e.target.value)"""
        ret_string += f"""<div className="p-6">\n"""
        if column['COLUMN_NAME'].split('/')[-1].lower() == 'path':
            ret_string += f"""
                      <Box className="mb-4">
                            <input
                                type="file"
                                accept="image/*"
                                onChange={{(e) =>
                                    setData(
                                        "image",
                                        e.target.files?.[0] || null
                                    )
                                }}
                                className="hidden"
                                id="{column['COLUMN_NAME']}-image-input"
                            />
                            <label htmlFor="{column['COLUMN_NAME']}-image-input">
                                <Button variant="contained" component="span">
                                    {utilities.any_case_to_title({column['COLUMN_NAME']})}
                                </Button>
                            </label>
                            {{errors.image && (
                                <Typography color="error">
                                    {{errors.image}}
                                </Typography>
                            )}}
                        </Box>\n\n"""
        else:
            table_name = utilities.get_table_name_from_fk_column_name(column['COLUMN_NAME'], belongs_to_list, ignore_columns)
            if utilities.remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
                ret_string += f"""                        <FormControl fullWidth className="mb-4">
                            <InputLabel>{utilities.any_case_to_title(utilities.remove_id_suffix(column['COLUMN_NAME']))}</InputLabel>
                            <Select
                                value={{data.{column['COLUMN_NAME']} }}
                                onChange={{(e) =>
                                    setData("{column['COLUMN_NAME']}", e.target.value as number)
                                }}
                                error={{!!errors.{column['COLUMN_NAME']}}}
                            >
                                {{{table_name}.map((item) => (
                                  <MenuItem key={{item.id}} value={{item.id}}>
                                    {{item.{model_utilities.get_first_text_like_column_from_table_name(connection, utilities.get_table_name_from_fk_column_name(column['COLUMN_NAME'], belongs_to_list, ignore_columns))} }}
                                  </MenuItem>
                                ))}}
                            </Select>
                            {{errors.{column['COLUMN_NAME']} && (
                                <Typography color="error">
                                    {{errors.{column['COLUMN_NAME']}}}
                                </Typography>
                            )}}
                        </FormControl>\n\n"""
            else:
                ret_string += f"""            <TextField
              fullWidth
              label="{utilities.any_case_to_title(column['COLUMN_NAME'])}"
              value={{data.{column['COLUMN_NAME']}}}
              onChange={{(e) => setData('{column['COLUMN_NAME']}', {target_value})}}
              error={{!!errors.{column['COLUMN_NAME']}}}
              helperText={{errors.{column['COLUMN_NAME']}}}
              className="my-4"
            />"""
        ret_string += "</div>"
    return ret_string


def get_foreign_key_interfaces(columns, ignore_columns, belongs_to_list):
    ret_string = ""
    for fk in belongs_to_list:
        if fk['column_name'] in ignore_columns:
            continue
        ret_string += f"""\ninterface {utilities.any_case_to_pascal_case(utilities.singular(fk['table_name']))} {{
  id: number;
  {fk['view_column']}: string
  }}\n"""
    return ret_string


def get_props_interface(columns, ignore_columns, belongs_to_list):
    ret_string = """interface Props {
    auth: Auth;
"""
    for fk in belongs_to_list:
        if fk['column_name'] in ignore_columns:
            continue
        ret_string += f"""    {fk['table_name']}: { utilities.any_case_to_pascal_case(utilities.singular(fk['table_name']))}[];\n"""

    ret_string += """  }"""
    return ret_string


def get_props_interfaces_as_csl(ignore_columns, belongs_to_list):
    ret_string = """auth  """
    for fk in belongs_to_list:
        if fk['column_name'] in ignore_columns:
            continue
        if utilities.remove_id_suffix(fk['column_name']) != fk['column_name']:
            ret_string += f""", {fk['table_name']}"""
    return ret_string
