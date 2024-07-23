from codegenerator.laravel_11 import utilities

def get_web_controller_file_content(ln, ci, belongs_to_list, has_many_list, has_many_through_list):
    controller_code = f"""<?php

namespace App\\Http\\Controllers;

use App\\Http\\Controllers\\Controller;
use App\\Models\\{ln.model_class_name};
use App\\Http\\Requests\\{ln.request_class_name};
use App\\Http\\Resources\\{ln.resource_class_name};
"""
    for item in belongs_to_list:
        controller_code += f"use App\\Http\\Requests\\{utilities.model_class_name_from_table_name(item['table_name'])}Request;\n"
        controller_code += f"use App\\Http\\Resources\\{utilities.model_class_name_from_table_name(item['table_name'])}Resource;\n"
    for item in has_many_list:
        controller_code += f"use App\\Http\\Requests\\{utilities.model_class_name_from_table_name(item['table_name'])}Request;\n"
        controller_code += f"use App\\Http\\Resources\\{utilities.model_class_name_from_table_name(item['table_name'])}Resource;\n"
    for item in has_many_through_list:
        controller_code += f"use App\\Http\\Requests\\{utilities.model_class_name_from_table_name(item['table'])}Request;\n"
        controller_code += f"use App\\Http\\Resources\\{utilities.model_class_name_from_table_name(item['table'])}Resource;\n"

    belongs_to_or_query = "query()"
    if len(belongs_to_list) > 0:
        # function_name = utilities.any_case_to_camel_case(s['column_name'].replace('_id', ''))
        comma_separated_list = ", ".join(f'"{utilities.any_case_to_camel_case(s["column_name"].replace("_id", ""))}"' for s in belongs_to_list)
        belongs_to_or_query = f"with([{comma_separated_list}])"

    controller_code += f"""
class {ln.web_controller_class_name} extends Controller
{{
    /**
     * Display a listing {ln.lcp}.
     *
     * @return \\Illuminate\\Http\\Response
     */
    public function index()
    {{
        $query = {ln.model_class_name}::{belongs_to_or_query};

        $sortField = request("sort_field", 'created_at');
        $sortDirection = request("sort_direction", "desc");
 """
    if len(belongs_to_list) > 0:
        controller_code += f"""
        if (in_array($sortField, [{comma_separated_list}])) {{
        $relation = explode('.', $sortField)[0];
        $column = explode('.', $sortField)[1];
        $query->join($relation, $relation.'.id', '=', 'workouts.'.$relation.'_id')
              ->orderBy($relation.'.'.$column, $sortDirection)
              ->select('workouts.*'); // Ensure we only select from the workouts table
        }} else {{
            $query->orderBy($sortField, $sortDirection);
        }}"""
    else:
        

    controller_code += f"""
        if (in_array($sortField, [{comma_separated_list}])) {{
        $relation = explode('.', $sortField)[0];
        $column = explode('.', $sortField)[1];
        $query->join($relation, $relation.'.id', '=', 'workouts.'.$relation.'_id')
              ->orderBy($relation.'.'.$column, $sortDirection)
              ->select('workouts.*'); // Ensure we only select from the workouts table
        }} else {{
            $query->orderBy($sortField, $sortDirection);
        }}
        
        

{ci.controller_index_where_statements}

        ${ln.lctn} = $query->orderBy($sortField, $sortDirection)
            ->paginate(10)
            ->onEachSide(1);

        return inertia("{ln.model_class_name}/Index", [
            "{ln.lctn}" => {ln.model_class_name}Resource::collection(${ln.lctn}),
            'queryParams' => request()->query() ?: null,
            'success' => session('success'),
        ]);
    }}

    
    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {{
        ${ln.lctn} = {ln.model_class_name}::query()->orderBy('name', 'asc')->get();
        $users = User::query()->orderBy('name', 'asc')->get();

        return inertia("{ln.model_class_name}/Create", [
            '{ln.lctn}' => {ln.model_class_name}Resource::collection(${ln.lctn}),
            'users' => UserResource::collection($users),
        ]);
    }}

    /**
     * Store a newly created resource in storage.
     */
    public function store(Store{ln.model_class_name}Request $request)
    {{
        $data = $request->validated();
        /** @var $image \\Illuminate\\Http\\UploadedFile */
        $image = $data['image'] ?? null;
        $data['created_by'] = Auth::id();
        $data['updated_by'] = Auth::id();
        if ($image) {{
            $data['image_path'] = $image->store('{ln.lcs}/' . Str::random(), 'public');
        }}
        {ln.model_class_name}::create($data);

        return to_route('{ln.lcs}.index')
            ->with('success', '{ln.model_class_name} was created');
    }}

    /**
     * Display the specified resource.
     */
    public function show({ln.model_class_name} ${ln.lcs})
    {{
        return inertia('{ln.model_class_name}/Show', [
            '{ln.lcs}' => new {ln.model_class_name}Resource(${ln.lcs}),
        ]);
    }}

    /**
     * Show the form for editing the specified resource.
     */
    public function edit({ln.model_class_name} ${ln.lcs})
    {{
        ${ln.lctn} = {ln.model_class_name}::query()->orderBy('name', 'asc')->get();
        $users = User::query()->orderBy('name', 'asc')->get();

        return inertia("{ln.model_class_name}/Edit", [
            '{ln.lcs}' => new {ln.model_class_name}Resource(${ln.lcs}),
            '{ln.lctn}' => {ln.model_class_name}Resource::collection(${ln.lctn}),
            'users' => UserResource::collection($users),
        ]);
    }}

    /**
     * Update the specified resource in storage.
     */
    public function update(Update{ln.model_class_name}Request $request, {ln.model_class_name} ${ln.lcs})
    {{
        $data = $request->validated();
        $image = $data['image'] ?? null;
        $data['updated_by'] = Auth::id();
        if ($image) {{
            if (${ln.lcs}->image_path) {{
                Storage::disk('public')->deleteDirectory(dirname(${ln.lcs}->image_path));
            }}
            $data['image_path'] = $image->store('{ln.lcs}/' . Str::random(), 'public');
        }}
        ${ln.lcs}->update($data);

        return to_route('{ln.lcs}.index')
            ->with('success', "{ln.model_class_name} \\"${ln.lcs}->name\\" was updated");
    }}

    /**
     * Remove the specified resource from storage.
     */
    public function destroy({ln.model_class_name} ${ln.lcs})
    {{
        $name = ${ln.lcs}->name;
        ${ln.lcs}->delete();
        if (${ln.lcs}->image_path) {{
            Storage::disk('public')->deleteDirectory(dirname(${ln.lcs}->image_path));
        }}
        return to_route('{ln.lcs}.index')
            ->with('success', "{ln.model_class_name} \\"$name\\" was deleted");
    }}
}}
    """
    return controller_code
