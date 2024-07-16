# ln=laravel names, ci= column info
def get_web_controller_file_content(ln, ci):
    controller_code = f"""<?php

namespace App\\Http\\Controllers;

use App\\Http\\Controllers\\Controller;
use App\\Models\\{ln.model_class_name};
use App\\Http\\Requests\\{ln.request_class_name};

class {ln.web_controller_class_name} extends Controller
{{
    /**
     * Display a listing {ln.lcp}.
     *
     * @return \\Illuminate\\Http\\Response
     */
    public function index()
    {{
        //redirect to the vue3 spa
    }}

    /**
     * Get the quick list of {ln.lcp}.
     *
     * @return \\Illuminate\\Support\\Collection
     */
    public function getQuickList()
    {{
        ${ln.lcs} = new {ln.request_class_name};
        return ${ln.lcs}->getQuickList();
    }}
}}
    """
    return controller_code
