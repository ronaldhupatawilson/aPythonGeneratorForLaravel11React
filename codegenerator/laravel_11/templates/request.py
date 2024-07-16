# ln=laravel names, ci= column info
def get_request_file_content(ln, ci):
    request_code = f"""<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
//use Illuminate\Validation\Rule;

class {ln.request_class_name} extends FormRequest
{{
    public function authorize()
    {{
        return true;
    }}

    public function rules()
    {{
        $method = $this->method();
        if($method == 'PUT')
        {{
            return [
{ci.request_validation_fields}
            ];
        }}
        else
        {{
            return [
{ci.request_patch_validation_fields}
            ];
        }}
    }}
    
    protected function prepareForValidation()
    {{
{ci.prepare_for_validation}
    }}
}}
    """
    return request_code
