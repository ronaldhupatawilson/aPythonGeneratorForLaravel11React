# ln=laravel names, ci= column info
def get_resource_file_content(ln, ci):
    resource_code = f"""<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class {ln.resource_class_name} extends JsonResource
{{
    /**
     * Preserve the collection keys.
     *
     * @var bool
     */
    public $preserveKeys = true;

    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {{
        return [
{ci.resource_array}
        ];
    }}
}}
    """
    return resource_code
