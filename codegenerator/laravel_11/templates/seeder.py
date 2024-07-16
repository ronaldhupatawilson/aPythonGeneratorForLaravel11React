# ln=laravel names, ci= column info
def get_seeder_file_content(ln, ci):
    seeder_code = f"""<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\{ln.model_class_name};

class {ln.model_class_name}TableSeeder extends Seeder
{{
    public function run()
    {{
        {ln.model_class_name}::factory()
            ->count(300)
            ->create();
    }}
}}
"""
    return seeder_code
