# ln=laravel names, ci= column info
def get_factory_file_content(ln, ci):
    factory_code = f"""<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class {ln.factory_class_name} extends Factory
{{

    public function definition(): array
    {{
        return [
{ci.faker_fields}
        ];
    }}
}}
    """
    return factory_code
