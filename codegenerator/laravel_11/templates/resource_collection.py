# ln=laravel names, ci= column info
def get_resource_collection_file_content(ln, ci):
    resource_collection_code = f"""<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\ResourceCollection;

class {ln.resource_collection_class_name} extends ResourceCollection
{{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<int|string, mixed>
     */
    public function toArray(Request $request): array
    {{
        return parent::toArray($request);
    }}
}}

    """
    return resource_collection_code
