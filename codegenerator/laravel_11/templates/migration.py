# ln=laravel names, ci= column info
def get_migration_file_content(ln, ci):
    migration_code = f"""<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{{
    /**
     * Run the migrations.
     */
    public function up(): void
    {{
        Schema::create('{ln.tn}', function (Blueprint $table) {{
{ci.migration_fields}
        }});
    }}
    
    /**
     * reverse the migrations.
     */
    public function down(): void
    {{
        Schema::dropIfExists('{ln.tn}');
    }}
}};
    """

    return migration_code
