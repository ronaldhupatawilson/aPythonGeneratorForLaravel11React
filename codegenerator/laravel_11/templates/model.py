from codegenerator.laravel_11 import utilities


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
    
    """

    if len(has_many_list) > 0:
        for many_related_table in has_many_list:
            model_code += (f"""
            
        public function {many_related_table}(): HasMany
        {{
            return $this->hasMany({utilities.any_case_to_pascal_case(utilities.singular(many_related_table))}::class);
        }}
            """)

    if len(belongs_to_list) > 0:
        for belongs_to_table in belongs_to_list:
            model_code += (f"""
            
        public function {belongs_to_table}(): BelongsTo
        {{
            return $this->belongsTo({utilities.any_case_to_pascal_case(utilities.singular(belongs_to_table))}::class);
        }}
            """)

    if len(has_many_through_list) > 0:
        for many_to_many_item in has_many_through_list:
            if isinstance(utilities.singular(many_to_many_item['table']), bool):
                foreign_table_model_name = many_to_many_item['table']
            else:
                foreign_table_model_name = utilities.singular(many_to_many_item['table'])

            model_code += (f"""
            
        public function {many_to_many_item['table']}(): BelongsToMany
        {{
            return $this->belongsToMany({utilities.any_case_to_pascal_case(foreign_table_model_name)}::class);
        }}
            """)

    model_code += """

}
    

"""
    return model_code
