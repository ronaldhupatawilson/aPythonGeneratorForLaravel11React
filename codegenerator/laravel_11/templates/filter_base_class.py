# ln=laravel names, ci= column info
def get_filter_base_class():
    filter_base_class_code = f"""<?php

namespace App\\Filters;

use Illuminate\\Http\\Request;

class ApiFilter
{{
    protected $safeParms = [];
    
    protected $columnMap = [];
    
    protected $operatorMap = [
        'eq' => '=',
        'lt' => '<',
        'lte' => '<=',
        'gt' => '>',
        'gte' => '>=',
        'neq' => '<>',
        'lk' => 'LIKE',
        'nlk' => 'NOT LIKE',
    ];

    /**
     * Transform the filter into an array of eloquent where arrays.
     *
     * @return array[['column','operator', 'value'],['column','operator', 'value'],...]
     */
    public function transform(Request $request): array
    {{
        $eloQuery = [];
        
        foreach($this->safeParms as $parm => $operators){{
            $query = $request->query($parm);
            
            if(!isset($query)) {{
                continue;
            }}
            
            $column = $this->columnMap[$parm] ?? $parm;
            
            foreach($operators as $operator) {{
                if (isset($query[$operator]) && isset($this->operatorMap[$operator])) {{
                    $queryVal = ($operator == 'lk' || $operator =='nlk') ? '%'.$query[$operator].'%': $query[$operator];
                    $eloQuery[] = [$column, $this->operatorMap[$operator], $queryVal];
                }}
            }}
        }}
        return $eloQuery;
    }}
}}
    """
    return filter_base_class_code

