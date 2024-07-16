from codegenerator.laravel_11 import utilities


class ColumnInfo:
    def __init__(self, columns, ignore_columns):
        self.faker_fields = utilities.get_column_faker_code(columns, ignore_columns)
        self.migration_fields = utilities.get_column_migration_code(columns)
        self.request_validation_fields = utilities.get_column_request_validation_field_code(columns, ignore_columns)
        self.request_patch_validation_fields = utilities.get_patch_column_request_validation_field_code(columns, ignore_columns)
        self.model_fillable_fields = utilities.get_column_fillable_field_code(columns, ignore_columns)
        self.first_non_null_column = utilities.get_first_non_null_column(columns, ignore_columns)
        self.first_nullable_textlike_column = utilities.get_first_nullable_textlike_column(columns, ignore_columns)
        self.comma_separated_list_of_column_names = utilities.get_comma_separated_list_of_column_names(columns, ignore_columns)
        self.primary_key_column = utilities.get_primary_key_column(columns)
        self.first_textlike_column = utilities.get_first_textlike_column(columns, ignore_columns)
        self.resource_array = utilities.get_resource_array(columns, ignore_columns)
        self.resource_collection_array = utilities.get_resource_collection_array(columns, ignore_columns)
        self.column_test_fields_fillable_as_associative_array = utilities.get_column_test_fields_fillable_as_associative_array(columns, ignore_columns)
        self.column_fillable_as_comma_separated_string = utilities.get_column_fillable_field_code(columns, ignore_columns)
        self.filter_column_map_arr = utilities.get_filter_column_map_arr(columns, ignore_columns)
        self.filter_safe_parms_arr = utilities.get_filter_safe_parms_arr(columns, ignore_columns)
        self.prepare_for_validation = utilities.get_prepare_for_validation(columns, ignore_columns)