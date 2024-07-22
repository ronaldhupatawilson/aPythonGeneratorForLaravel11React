# ln=laravel names, ci= column info
def get_generated_routes(imports, routes):
    code = f"""<?php

use Illuminate\\Foundation\\Application;
use Illuminate\\Support\\Facades\\Route;
use Inertia\\Inertia;
"""
    for importStrings in imports:
        code += importStrings

    code += """

Route::middleware(['auth', 'verified'])->group(function () {{

"""
    for route in routes:
        code += route

    code += """

}});
    """
    return code

