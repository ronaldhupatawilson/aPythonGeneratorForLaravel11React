from codegenerator.laravel_11 import utilities
# from pprint import pprint


def get_model_file_content(ln, ci, belongs_to_list, has_many_list, has_many_through_list ):
    extended_class = 'Model'
    use_class = "Illuminate\\Database\\Eloquent\\Model"
    # s = ln.tn
    # if lambda s: '_' in s:
    #     extended_class = 'Pivot'
    #     use_class = "Illuminate\\Database\\Eloquent\\Relations\\Pivot"

    model_code = f"""<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use {use_class};
"""

    if len(belongs_to_list) > 0:
        model_code += """use Illuminate\\Database\\Eloquent\\Relations\\BelongsTo;
"""

    if len(has_many_list) > 0:
        model_code += """use Illuminate\\Database\\Eloquent\\Relations\\HasMany;
"""

    if len(has_many_through_list) > 0:
        model_code += """use Illuminate\\Database\\Eloquent\\Relations\\BelongsToMany;
"""
    model_code += f"""

class {ln.model_class_name} extends {extended_class}
{{
    use HasFactory;
    
    protected $table = '{ln.tn}';
    
    protected $fillable = [{ci.model_fillable_fields}];
    
    """

    if len(has_many_list) > 0:
        for many_related_table in has_many_list:
            replace_text = f"{ln.lcs}_id"
            suffix = many_related_table['column_name'].replace(replace_text, '')
            model_code += (f"""
            
    public function {many_related_table['table_name'].strip('_')}{suffix}(): HasMany
    {{
        return $this->hasMany({utilities.any_case_to_pascal_case(utilities.singular(many_related_table['table_name']))}::class, '{many_related_table['column_name']}');
    }}
            """)

    if len(belongs_to_list) > 0:
        for belongs_to_table in belongs_to_list:
            singular_table_name = utilities.singular(belongs_to_table['table_name'])
            function_name = utilities.any_case_to_camel_case(belongs_to_table['column_name'].replace('_id', ''))
            model_code += (f"""
            
    public function {function_name}(): BelongsTo
    {{
        return $this->belongsTo({utilities.any_case_to_pascal_case(singular_table_name)}::class, '{belongs_to_table['column_name']}');
    }}
            """)

    if len(has_many_through_list) > 0:
        for many_to_many_item in has_many_through_list:
            foreign_table_model_name = utilities.singular(many_to_many_item['table_name'])

            if len(many_to_many_item['columns']) > 0:
                with_pivot = f"->withPivot({many_to_many_item['columns']})"
            else:
                with_pivot = ''
            # you can specify a Model to use as the intermediate table - see https://laravel.com/docs/11.x/eloquent-relationships#syncing-associations - Defining Custom Intermediate Table Models
            model_code += (f"""
            
    public function {many_to_many_item['table_name']}(): BelongsToMany
    {{
        return $this->belongsToMany({utilities.any_case_to_pascal_case(foreign_table_model_name)}::class, '{"_".join(sorted([many_to_many_item['table_name'], ln.tn]))}'){with_pivot};
    }}
            """)

    model_code += """

}
    

"""
    return model_code
