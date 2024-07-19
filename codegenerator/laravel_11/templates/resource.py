from codegenerator.laravel_11 import utilities


def get_resource_file_content(ln, ci):
    carbon_import = ''
    storage_import = ''
    if ci.has_dates_or_times:
        carbon_import = 'use Carbon\\Carbon;'
    if ci.has_storage_path:
        storage_import = 'use Illuminate\\Support\\Facades\\Storage;'
    resource_code = f"""<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\JsonResource;
{carbon_import}
{storage_import}

class {ln.resource_class_name} extends JsonResource
{{
    /**
     * Preserve the collection keys.
     *
     * @var bool
     */
    public $preserveKeys = true;
    
    /**
     * removes envelope from passed in data
     */
    public static $wrap = false;

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
