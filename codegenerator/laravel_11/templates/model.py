from codegenerator.laravel_11 import utilities
# from pprint import pprint


def get_model_file_content(ln, ci, belongs_to_list, has_many_list, has_many_through_list ):
    model_code = f"""<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;
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

class {ln.model_class_name} extends Model
{{
    use HasFactory;
    
    protected $table = '{ln.tn}';
    
    protected $fillable = [{ci.model_fillable_fields}];

    /**
     * Any columns that should be hidden for serialization - place them in this array and uncomment.
     */
    /*protected $hidden = [{ci.model_fillable_fields}];*/
    
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
            if isinstance(utilities.singular(belongs_to_table['table_name']), bool):
                singular_table_name = belongs_to_table['table_name']
            else:
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
            if isinstance(utilities.singular(many_to_many_item['table']), bool):
                foreign_table_model_name = many_to_many_item['table']
            else:
                foreign_table_model_name = utilities.singular(many_to_many_item['table'])

            if len(many_to_many_item['columns']) > 0:
                with_pivot = f"->withPivot({many_to_many_item['columns']})"
            else:
                with_pivot = ''
            model_code += (f"""
            
    public function {many_to_many_item['table']}(): BelongsToMany
    {{
        return $this->belongsToMany({utilities.any_case_to_pascal_case(foreign_table_model_name)}::class){with_pivot};
    }}
            """)

    model_code += """

}
    

"""
    return model_code
