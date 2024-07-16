# ln=laravel names, ci= column info
def get_filter_file_content(ln, ci):
    filter_code = f"""<?php

namespace App\\Filters;

use App\\Filters\\ApiFilter;

class {ln.filter_class_name} extends ApiFilter
{{
    protected $safeParms = [
{ci.filter_safe_parms_arr}   
    ];
    
    protected $columnMap = [
{ci.filter_column_map_arr}   
    ];
}}
    """
    return filter_code
