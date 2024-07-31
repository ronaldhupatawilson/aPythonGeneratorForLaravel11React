import inflect
import re
from mysql.connector.connection import MySQLConnection
from codegenerator.laravel_11 import model_utilities
from pprint import pprint

p = inflect.engine()


def uncapitalize_first_letter(s):
    return s[:1].lower() + s[1:] if s else s


def capitalize_first_letter(s):
    return s[:1].upper() + s[1:] if s else s


def singular(noun):
    return_value = p.singular_noun(noun)
    if isinstance(return_value, bool):
        return_value = noun
    return return_value


def plural(noun):
    return_value = p.plural(noun)
    if isinstance(return_value, bool):
        return_value = noun
    return return_value


def lower_case_single(noun):
    return singular(noun.lower())


def model_class_name_from_table_name(some_table_name):
    return any_case_to_pascal_case(singular(some_table_name))


def cap_first_single(noun):
    if singular( noun.lower() ) :
        single_lowercase_noun = singular(noun.lower())
    else:
        single_lowercase_noun = noun
    return single_lowercase_noun.title()


def lower_case_plural(noun):
    return plural(noun.lower())


def cap_first_plural(noun):
    plural_lowercase_noun = plural(noun.lower())
    return plural_lowercase_noun.title()


def any_case_to_title(word):
    underscores_removed = word.replace("_", " ")
    hyphens_removed = underscores_removed.replace("-", " ")
    regex = re.compile(r"([A-Z])")
    camel_or_pascal_case_split = regex.sub(r" \1", hyphens_removed)
    trimmed = camel_or_pascal_case_split.strip()
    return trimmed.title()


def any_case_to_pascal_case(word):
    underscores_removed = word.replace("_", " ")
    hyphens_removed = underscores_removed.replace("-", " ")
    trimmed = hyphens_removed.strip()
    spaced = trimmed.title()
    return spaced.replace(" ", "")


def any_case_to_camel_case(word):
    underscores_removed = word.replace("_", " ")
    hyphens_removed = underscores_removed.replace("-", " ")
    trimmed = hyphens_removed.strip()
    spaced = trimmed.title()
    pascal_case = spaced.replace(" ", "")
    return pascal_case[0].lower() + pascal_case[1:]


def mysql_field_to_faker_function_mapper(column):
    if column['COLUMN_KEY'] == 'PRI':
        return 'fake()->numberBetween(1, 300)'
    if column['DATA_TYPE'] == 'varchar' or column['DATA_TYPE'] == 'char':
        return f"fake()->text({column['CHARACTER_MAXIMUM_LENGTH']})"
    if column['DATA_TYPE'] == 'bigint' or column['DATA_TYPE'] == 'int' or column['DATA_TYPE'] == 'smallint':
        return 'fake()->numberBetween(1, 300)'
    if column['DATA_TYPE'] == 'text' or column['DATA_TYPE'] == 'mediumtext' or column['DATA_TYPE'] == 'longtext':
        return 'fake()->sentence()'
    if column['DATA_TYPE'] == 'date':
        return 'fake()->date()'
    if column['DATA_TYPE'] == 'datetime':
        return 'fake()->dateTime()'
    if column['DATA_TYPE'] == 'timestamp':
        return 'fake()->unixTime'
    if column['DATA_TYPE'] == 'time':
        return 'fake()->time()'
    if column['DATA_TYPE'] == 'decimal' or column['DATA_TYPE'] == 'float' or column['DATA_TYPE'] == 'double':
        return f"fake()->randomFloat({column['NUMERIC_SCALE']}, 0, 100)"
    if column['DATA_TYPE'] == 'tinyint':
        return "fake()->numberBetween(0, 1)"
    return "fake()->numberBetween(0, 1)"


def get_column_faker_code(columns, ignore_columns):
    # 'muscleGroup_id' => faker()->numberBetween(1, 300),
    # 'exercise' => faker()->words(3, true),
    # 'exerciseDescription' => faker()->sentence(),
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        faker_code = mysql_field_to_faker_function_mapper(column)
        return_string += " " * 12 + f"'{column['COLUMN_NAME']}' => {faker_code},\n"
    return return_string


def get_string_before_parenthesis(string):
    string = str(string)
    opening_parenthesis_index = string.find("(")
    if opening_parenthesis_index == -1:
        return string
    else:
        return string[:opening_parenthesis_index]


def mysql_field_to_migration_mapper(column):
    column_name = column['COLUMN_NAME']
    data_type_in_bytes = column['COLUMN_TYPE']
    data_type_str = get_string_before_parenthesis(data_type_in_bytes)
    unsigned = data_type_str.find(' unsigned') > -1
    nullable = column['IS_NULLABLE'] == 'YES'
    return_string = ''
    if column['COLUMN_KEY'] == 'PRI':
        if column['DATA_TYPE'] == 'int':
            return_string += f"increments('{column_name}')"
        elif column['DATA_TYPE'] == 'tinyint':
            return_string += f"tinyIncrements('{column_name}')"
        elif column['DATA_TYPE'] == 'smallint':
            return_string += f"smallIncrements('{column_name}')"
        elif column['DATA_TYPE'] == 'mediumint':
            return_string += f"mediumIncrements('{column_name}')"
        else:
            return_string += f"bigIncrements('{column_name}')"
    else:
        if column['DATA_TYPE'] == 'varchar':
            return_string += f"string('{column_name}',{column['CHARACTER_MAXIMUM_LENGTH']})"
        if column['DATA_TYPE'] == 'char':
            return_string += f"char('{column_name}',{column['CHARACTER_MAXIMUM_LENGTH']})"
        if column['DATA_TYPE'] == 'bigint':
            if unsigned :
                return_string += f"unsignedBigInteger('{column_name}')"
            else:
                return_string += f"bigInteger('{column_name}')"
        if column['DATA_TYPE'] == 'int':
            if unsigned :
                return_string += f"unsignedInteger('{column_name}')"
            else:
                return_string += f"integer('{column_name}')"
        if column['DATA_TYPE'] == 'mediumint':
            if unsigned :
                return_string += f"unsignedMediumInteger('{column_name}')"
            else:
                return_string += f"mediumInteger('{column_name}')"
        if column['DATA_TYPE'] == 'smallint':
            if unsigned :
                return_string += f"unsignedSmallInteger('{column_name}')"
            else:
                return_string += f"smallInteger('{column_name}')"
        if column['DATA_TYPE'] == 'tinyint':
            if unsigned :
                return_string += f"unsignedTinyInteger('{column_name}')"
            else:
                return_string += f"tinyInteger('{column_name}')"
        if column['DATA_TYPE'] == 'text':
            return_string += f"text('{column_name}')"
        if column['DATA_TYPE'] == 'mediumtext':
            return_string += f"mediumText('{column_name}')"
        if column['DATA_TYPE'] == 'longtext':
            return_string += f"longText('{column_name}')"
        if column['DATA_TYPE'] == 'date':
            return_string += f"date('{column_name}')"
        if column['DATA_TYPE'] == 'datetime':
            return_string += f"dateTime('{column_name}')"
        if column['DATA_TYPE'] == 'timestamp':
            return_string += f"timestamp('{column_name}')"
        if column['DATA_TYPE'] == 'time':
            return_string += f"time('{column_name}')"
        if column['DATA_TYPE'] == 'decimal':
            if unsigned :
                return_string += f"unsignedDecimal('{column_name}',{column['NUMERIC_PRECISION']},{column['NUMERIC_SCALE']}"
            else:
                return_string += f"decimal('{column_name}',{column['NUMERIC_PRECISION']},{column['NUMERIC_SCALE']})"
        if column['DATA_TYPE'] == 'float':
            return_string += f"float('{column_name}',{column['NUMERIC_PRECISION']},{column['NUMERIC_SCALE']})"
        if column['DATA_TYPE'] == 'double':
            return_string += f"double('{column_name}',{column['NUMERIC_PRECISION']},{column['NUMERIC_SCALE']})"

    if nullable or column['DATA_TYPE'] == 'timestamp':
        return_string += "->nullable()"

    if column['COLUMN_DEFAULT'] != 'NULL' and column['COLUMN_DEFAULT'] is not None:
        if column['DATA_TYPE'] in ['int', 'timestamp', 'bigint', 'mediumint', 'smallint', 'tinyint', 'decimal', 'float', 'double']:
            if column['DATA_TYPE'] != 'timestamp':
                return_string += f"->default({column['COLUMN_DEFAULT']})"
            # else:
            #     if column['COLUMN_DEFAULT'] == '0000-00-00 00:00:00':
            #         #return_string += f"->default(0)"
            #
            #     if column['COLUMN_DEFAULT'] == 'current_timestamp()':
            #         #return_string += f"->default(DB::raw('CURRENT_TIMESTAMP()'))"
        else:
            return_string += f"->default('{column['COLUMN_DEFAULT']}')"

    return return_string


def get_column_migration_code(columns):
    # $table->id();
    # $table->unsignedBigInteger('muscleGroup_id')->nullable();
    # $table->string('exercise');
    # $table->text('exerciseDescription')->nullable();
    # $table->timestamps();
    return_string = ''
    for column in columns:
        migration_code = mysql_field_to_migration_mapper(column)
        return_string += " " * 12 + f"$table->{migration_code};\n"
    return return_string


# @todo - this could have better separation of allowable field lengths
def mysql_field_to_validation_mapper(column):
    return_string = 'required'
    if column['IS_NULLABLE'] == 'YES':
        return_string = 'nullable'
    if column['DATA_TYPE'] == 'varchar' or column['DATA_TYPE'] == 'char':
        return_string += f"|string|max:{column['CHARACTER_MAXIMUM_LENGTH']}"
    if column['DATA_TYPE'] == 'bigint' or column['DATA_TYPE'] == 'int' or column['DATA_TYPE'] == 'smallint':
        return_string += f"|integer"
    if column['DATA_TYPE'] == 'text' or column['DATA_TYPE'] == 'mediumtext' or column['DATA_TYPE'] == 'longtext':
        return_string += f"|string"
    if column['DATA_TYPE'] == 'date':
        return_string += f"|date"
    # if column['DATA_TYPE'] == 'datetime':
    #     return_string += f"|"
    # if column['DATA_TYPE'] == 'timestamp':
    #     return_string += f"|"
    # if column['DATA_TYPE'] == 'time':
    #     return_string += f"|"
    if column['DATA_TYPE'] == 'decimal' or column['DATA_TYPE'] == 'float' or column['DATA_TYPE'] == 'double':
        return_string += "|numeric"
    if column['DATA_TYPE'] == 'tinyint':
        return_string += "|min:0|max:1"
    second_last = pluralize_second_to_last(column['COLUMN_NAME'])
    if second_last != column['COLUMN_NAME']:
        return_string += f"|exists:{second_last},id"
    else:
        if column['FK_TABLE'] is not None:
            return_string += f"|exists:{column['FK_TABLE']},{column['FK_COLUMN']}"
    return return_string


def pluralize_second_to_last(s):
    p = inflect.engine()
    parts = s.split('_')
    if len(parts) >= 2 and s[-3:] == '_id':
        return plural(parts[-2])
    return s


def get_column_request_validation_field_code(columns, ignore_columns):
    # 'muscleGroup_id' => 'nullable|integer',
    # 'exercise' => 'required|string|max:255',
    # 'exerciseDescription' => 'nullable|string'
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        validation_code = mysql_field_to_validation_mapper(column)
        return_string += " " * 16 + f"'{column['COLUMN_NAME']}' => '{validation_code}',\n"
    return return_string


def get_post_column_request_validation_field_code(columns, ignore_columns):
    # 'muscleGroup_id' => 'nullable|integer',
    # 'exercise' => 'required|string|max:255',
    # 'exerciseDescription' => 'nullable|string'
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME']  == 'id':
            continue
        validation_code = f"sometimes|{mysql_field_to_validation_mapper(column)}"
        return_string += " " * 16 + f"'{column['COLUMN_NAME']}' => '{validation_code}',\n"
    return return_string


def get_column_fillable_field_code(columns, ignore_columns):
    # 'muscleGroup_id',
    # 'exercise',
    # 'exerciseDescription'
    return_string = ''
    is_first = True
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if not is_first:
            return_string += ", "
        return_string += f"'{column['COLUMN_NAME']}'"
        is_first = False
    return return_string


def get_column_test_fields_fillable_as_associative_array(columns, ignore_columns):
    # 'first_name' => 'The',
    # 'last_name' => 'Terminator',
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        faker_code = mysql_field_to_faker_function_mapper(column)
        return_string += " " * 4 + f"'{column['COLUMN_NAME']}'=>{faker_code},\n"
    return return_string


def get_first_non_null_column(columns, ignore_columns):
    # first_name
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['IS_NULLABLE'] == 'YES':
            return column['COLUMN_NAME']
    return "/* @TODO NO NULLABLE FIELDS IN TABLE */"


def get_primary_key_column(columns):
    for column in columns:
        if column['COLUMN_KEY'] == 'PRI':
            return column['COLUMN_NAME']
    return "id"


def get_first_nullable_textlike_column(columns, ignore_columns):
    # first_name
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['DATA_TYPE'] == 'varchar' and column['IS_NULLABLE'] == 'YES':
            return column['COLUMN_NAME']
    return get_primary_key_column(columns)


def get_first_textlike_column(columns, ignore_columns):
    # first_name
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['DATA_TYPE'] in ['varchar', 'char', 'smalltext', 'text', 'mediumtext', 'largetext']:
            return column['COLUMN_NAME']
    return get_primary_key_column(columns)


def get_comma_separated_list_of_column_names(columns, ignore_columns):
    # 'first_name',
    # 'last_name',
    # 'date_of_birth',
    # 'email',
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        return_string += " " * 4 + f"'{column['COLUMN_NAME']}',\n"
    return return_string


def has_column_name_ending_in_path(list_of_dicts):
    for item in list_of_dicts:
        if isinstance(item, dict) and 'COLUMN_NAME' in item:
            column_name = item['COLUMN_NAME']
            if column_name.endswith('_path') or column_name.endswith('Path'):
                return True
    return False


def has_column_with_data_or_time_like_data_type(list_of_dicts):
    time_types = {'date', 'datetime', 'timestamp', 'time'}
    for item in list_of_dicts:
        if isinstance(item, dict) and 'DATA_TYPE' in item:
            data_type = item['DATA_TYPE'].lower()
            if data_type in time_types:
                return True
    return False


def get_resource_array(columns, ignore_columns, belongs_to_list, has_many_list, has_many_through_list, ln):
    time_types = {'date', 'datetime', 'timestamp', 'time'}
    # 'id' => $this->id,
    # 'name' => $this->name,
    # 'email' => $this->email,
    # 'created_at' => $this->created_at,
    # 'updated_at' => $this->updated_at,
    return_string = ''
    for column in columns:
        prefix = ''
        if column['COLUMN_NAME'] in ignore_columns:
            prefix = '//'
        return_string += " " * 12 + f"{prefix}'{column['COLUMN_NAME']}' => "
        if column['DATA_TYPE'] in time_types:
            date_time_format = 'Y-m-d H:i:s.u'
            if column['DATA_TYPE'] == 'date':
                date_time_format = 'Y-m-d'
            if column['DATA_TYPE'] == 'datetime':
                date_time_format = 'Y-m-d H:i:s'
            if column['DATA_TYPE'] == 'time':
                date_time_format = 'H:i:s'
            return_string += f"(new Carbon($this->{column['COLUMN_NAME']}))->format('{date_time_format}'),\n"
        else:
            if column['COLUMN_NAME'].endswith('_path') or column['COLUMN_NAME'].endswith('Path'):
                return_string += f"$this->{column['COLUMN_NAME']} && !(str_starts_with($this->{column['COLUMN_NAME']}, 'http')) ? Storage::url($this->{column['COLUMN_NAME']}) : '',\n"
            else:
                return_string += f"$this->{column['COLUMN_NAME']},\n"
    if len(belongs_to_list) > 0:
        for belongs_to_item in belongs_to_list:
            as_name = get_as_name_for_fk_col(belongs_to_item['column_name'], belongs_to_list)
            return_string += ' ' * 11 + f"""
            '{any_case_to_camel_case(belongs_to_item['table_name'])}' => new {any_case_to_pascal_case(singular(belongs_to_item['table_name']))}Resource($this->{any_case_to_camel_case(singular(belongs_to_item['table_name']))}),
            '{as_name}' => $this->{as_name},\n"""

    if len(has_many_list) > 0:
        for has_many_item in has_many_list:
            as_name = get_as_name_for_fk_col(has_many_item['column_name'], has_many_list)
            return_string += ' ' * 11 + f"""
            '{any_case_to_camel_case(has_many_item['table_name'])}' => new {any_case_to_pascal_case(singular(has_many_item['table_name']))}Resource($this->{any_case_to_camel_case(singular(has_many_item['table_name']))}),\n"""

    # if len(has_many_through_list) > 0:
    #     for has_many_through_item in has_many_through_list:
    #         tn = has_many_through_item['table_name']
    #         return_string += ' ' * 11 + f"""'{tn}' => {singular(tn)}Resource::collection($this->{tn}),\n"""

    return return_string


def get_resource_collection_array(columns, ignore_columns):
    # 'id' => $this->id,
    # 'name' => $this->name,
    # 'email' => $this->email,
    # 'created_at' => $this->created_at,
    # 'updated_at' => $this->updated_at,
    return_string = ''
    for column in columns:
        # if column['COLUMN_NAME'] in ignore_columns:
        #     continue
        return_string += " " * 12 + f"'{any_case_to_camel_case(column['COLUMN_NAME'])}' => $this->{column['COLUMN_NAME']},\n"
    return return_string


def get_filter_column_map_arr(columns, ignore_columns):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        return_string += " " * 8 + f"'{any_case_to_camel_case(column['COLUMN_NAME'])}' => '{column['COLUMN_NAME']}',\n"
    return return_string


def get_filter_safe_parms_arr(columns, ignore_columns):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        return_string += " " * 8 + f"'{column['COLUMN_NAME']}' => ['eq','ne'"
        if column['DATA_TYPE'] in ['int', 'bigint', 'mediumint', 'smallint', 'date', 'datetime', 'time', 'timestamp', 'decimal', 'double', 'float', 'real']:
            return_string += ",'gt' ,'gte' ,'lt' ,'lte'"
        if column['DATA_TYPE'] in ['char', 'varchar', 'text', 'smalltext', 'mediumtext', 'largetext']:
            return_string += ",'lk' ,'nlk'"
        return_string += "],\n"
    return return_string


def get_prepare_for_validation(columns, ignore_columns):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] != any_case_to_camel_case(column['COLUMN_NAME']):
            return_string += " " * 8 + f"if($this->{any_case_to_camel_case(column['COLUMN_NAME'])})\n"
            return_string += " " * 8 + "{\n"
            return_string += " " * 12 + "$this->merge([\n"
            return_string += " " * 12 + f"'{column['COLUMN_NAME']}' => $this->{any_case_to_camel_case(column['COLUMN_NAME'])}\n"
            return_string += " " * 8 + f"]);\n"
            return_string += " " * 8 + "}\n"
    return return_string


def get_typescript_interface_fields(columns, ignore_columns):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        typescript_type=""
        if column['DATA_TYPE'] in ['int', 'bigint', 'mediumint', 'smallint', 'decimal', 'double', 'float', 'real']:
            typescript_type += "number"
        if column['DATA_TYPE'] in ['char', 'varchar', 'text', 'longtext', 'mediumtext', 'smalltext', 'date', 'datetime', 'time', 'timestamp']:
            typescript_type += "string"
        if column['DATA_TYPE'] in ['tinyint']:
            typescript_type += "bool"
        return_string += " " * 4 + f"{column['COLUMN_NAME']}: {typescript_type};\n"
    return return_string


def get_controller_index_where_statements(columns, ignore_columns):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] == 'id':
            continue
        if column['COLUMN_NAME'][-3:] == '_id':
            continue
        return_string +=  " " * 8 + f"""if (request('{column['COLUMN_NAME']}')) {{\n"""
        if column['DATA_TYPE'] in ['int', 'bigint', 'mediumint', 'smallint', 'decimal', 'double', 'float', 'real', 'date', 'datetime', 'time', 'timestamp']:
            return_string += " " * 12 + f"""$query->where("{column['COLUMN_NAME']}", request("{column['COLUMN_NAME']}"));\n"""
        if column['DATA_TYPE'] in ['char', 'varchar', 'text', 'longtext', 'mediumtext', 'smalltext']:
            return_string += " " * 12 + f"""$query->where("{column['COLUMN_NAME']}", "like", "%" . request("{column['COLUMN_NAME']}") ."%");\n"""
        if column['DATA_TYPE'] in ['tinyint']:
            return_string += " " * 12 + f"""$query->where("{column['COLUMN_NAME']}", request("{column['COLUMN_NAME']}"));\n"""
        return_string += " " * 8 + f"""}}\n"""
    return return_string


def get_react_index_table_headings(columns, ignore_columns, belongs_to_list):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] == 'id':
            continue
        col_name = column['COLUMN_NAME']
        if remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
            col_name = get_as_name_for_fk_col(column['COLUMN_NAME'], belongs_to_list)
        return_string += " " * 20 + f"""<TableHeading
                      name="{col_name}"
                      sort_field={{mergedQueryParams.sort_field}}
                      sort_direction={{mergedQueryParams.sort_direction}}
                      sortChanged={{sortChanged}}
                    >
                      {any_case_to_title(remove_id_suffix(column['COLUMN_NAME']))}
                    </TableHeading>\n"""
    return return_string


def join_table_name(table1, table2):
    # Remove any leading/trailing whitespace and convert to lowercase
    table1 = table1.strip().lower()
    table2 = table2.strip().lower()
    # Check if inputs are valid (not empty and contain only letters)
    if not table1.isalpha() or not table2.isalpha():
        raise ValueError("Both inputs must be words containing only letters")
    return "_".join(sorted([table1, table2]))


def get_react_index_table_search_headings(columns, ignore_columns, belongs_to_list):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] == 'id':
            continue
        col_name = column['COLUMN_NAME']
        tab_name = column['COLUMN_NAME']
        if remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
            col_name = get_as_name_for_fk_col(column['COLUMN_NAME'], belongs_to_list)
            tab_name = get_table_name_from_fk_column_name(column['COLUMN_NAME'], belongs_to_list, ignore_columns)
        return_string += " " * 20 + f"""<TableCell>
                                            <TextField
                                                fullWidth
                                                defaultValue={{
                                                    queryParams?.{col_name} ?? ""
                                                }}
                                                placeholder="{any_case_to_title(singular(tab_name))}"
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


def react_index_table_data_cells(columns, ignore_columns, table_name, belongs_to_list):
    return_string = ''
    for column in columns:
        if column['COLUMN_NAME'] in ignore_columns:
            continue
        if column['COLUMN_NAME'] == 'id':
            continue
        col_name = column['COLUMN_NAME']
        if remove_id_suffix(column['COLUMN_NAME']) != column['COLUMN_NAME']:
            col_name = get_as_name_for_fk_col(column['COLUMN_NAME'], belongs_to_list)
        return_string += " " * 20 + f"""<TableCell>
                      {{ {table_name}.{col_name} }}
                    </TableCell>\n"""
    return return_string


def remove_id_suffix(s):
    return s[:-3] if s.endswith('_id') else s


def get_as_name_for_fk_col(foreign_key_column_name, fk_list):
    for fk in fk_list:
        if fk['column_name'] == foreign_key_column_name:
            cap_string = f"{fk['table_name']}{fk['view_column']}"
            return any_case_to_camel_case(cap_string)
    return foreign_key_column_name


def get_table_name_from_fk_column_name(column_name, belongs_to_list, ignore_columns):
    for column in belongs_to_list:
        if column['column_name'] in ignore_columns:
            continue
        if column['column_name'] == column_name:
            return column['table_name']
    return


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


def get_interface_info_from_table_name(connection: MySQLConnection, table_name: str, ignore_columns):
    cursor = connection.cursor()
    query = """
    SELECT COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
    WHERE COLUMNS.TABLE_NAME = %s
    AND COLUMNS.TABLE_SCHEMA = %s
    AND TABLES.TABLE_TYPE = 'BASE TABLE'
    ORDER BY COLUMNS.ORDINAL_POSITION
    """

    cursor.execute(query, (table_name, connection.database))
    results = cursor.fetchall()

    return_string = f"interface {any_case_to_camel_case(singular(table_name))} {{\n"

    for row in results:
        column_name = row[0]
        if column_name in ignore_columns:
            continue
        data_type = row[1]
        typescript_type = get_typescript_type_from_column_type(data_type)
        return_string += f"    {column_name}: {typescript_type};\n"

    return_string += "}\n"
    cursor.close()
    return return_string


def get_interface_info_from_table_name_with_belongs_to_list(connection: MySQLConnection, table_name: str, ignore_columns):
    belongs_to_list = model_utilities.belongs_to(connection, table_name)
    cursor = connection.cursor()
    query = """
    SELECT COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS JOIN INFORMATION_SCHEMA.TABLES ON (COLUMNS.TABLE_NAME = TABLES.TABLE_NAME AND COLUMNS.TABLE_SCHEMA = TABLES.TABLE_SCHEMA)
    WHERE COLUMNS.TABLE_NAME = %s
    AND COLUMNS.TABLE_SCHEMA = %s
    AND TABLES.TABLE_TYPE = 'BASE TABLE'
    ORDER BY COLUMNS.ORDINAL_POSITION
    """

    cursor.execute(query, (table_name, connection.database))
    results = cursor.fetchall()

    return_string = f"interface {any_case_to_camel_case(singular(table_name))} {{\n"

    for row in results:
        column_name = row[0]
        if column_name in ignore_columns:
            continue
        data_type = row[1]
        typescript_type = get_typescript_type_from_column_type(data_type)
        return_string += f"    {column_name}: {typescript_type};\n"
    for belongs_to_item in belongs_to_list:
        table_name = belongs_to_item['table_name']
        first_text_col = model_utilities.get_first_text_like_column_from_table_name(connection, table_name)
        return_string += f"    {table_name}{first_text_col}: string;\n"
    return_string += "}\n"
    cursor.close()
    return return_string
