from codegenerator.laravel_11 import utilities
from codegenerator.laravel_11 import model_utilities
from codegenerator.laravel_11 import controller_utilities


def get_web_controller_file_content(ln, ci,columns, ignore_columns, belongs_to_list, has_many_list, has_many_through_list, connection):
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
        controller_code += f"use App\\Models\\{utilities.model_class_name_from_table_name(item['table_name'])};\n"
    for item in has_many_list:
        controller_code += f"use App\\Http\\Requests\\{utilities.model_class_name_from_table_name(item['table_name'])}Request;\n"
        controller_code += f"use App\\Http\\Resources\\{utilities.model_class_name_from_table_name(item['table_name'])}Resource;\n"
    for item in has_many_through_list:
        controller_code += f"use App\\Http\\Resources\\{utilities.model_class_name_from_table_name(utilities.join_table_name(item['table_name'],ln.tn))}Resource;\n"
        controller_code += f"use App\\Models\\{utilities.model_class_name_from_table_name(utilities.join_table_name(item['table_name'],ln.tn))};\n"

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
        $sortField = request("sort_field", 'created_at');
        $sortDirection = request("sort_direction", "desc");
        $query = {ln.model_class_name}::query();

 """
    request_ref = []
    if len(belongs_to_list) > 0:
        select_ref = []
        is_first = True
        controller_code += f"""
        $query"""
        for fk_info in belongs_to_list:
            if not is_first:
                controller_code += ' ' * 12
            controller_code += f"""->leftJoin('{fk_info['table_name']}','{fk_info['table_name']}.id', '=', '{ln.tn}.{fk_info['column_name']}')\n"""
            sql_real_ref = f"""{fk_info['table_name']}.{fk_info['view_column']}"""
            as_name = f"""{utilities.any_case_to_camel_case(fk_info['table_name']+fk_info['view_column'])}"""
            select_ref_item = f"""'{sql_real_ref} as {as_name}'"""
            select_ref.append(select_ref_item)
            meta = {"actual_sql_ref": sql_real_ref, "as_name": as_name}
            request_ref.append(meta)
            is_first = False
        comma_separated_list = ", ".join(select_ref)
        controller_code += ' ' * 12  + f"""->select ('{ln.tn}.*', {comma_separated_list});"""
    controller_code += f"""

{ci.controller_index_where_statements}
"""
    if len(request_ref) > 0:
        for new_as_name in request_ref:
            controller_code +=  " " * 8 + f"""if (request('{new_as_name['as_name']}')) {{
                $query->where("{new_as_name['actual_sql_ref']}", "like", "%" . request("{new_as_name['as_name']}") ."%");
        }}\n\n"""
    controller_code += f"""
        ${ln.lctn} = $query->orderBy($sortField, $sortDirection)
            ->paginate(20)
            ->onEachSide(1);

        return inertia("{ln.model_class_name}/Index", [
            "{ln.lctn}" => {ln.model_class_name}Resource::collection(${ln.lctn}),\n"""
    controller_code += f"""
            'queryParams' => request()->query() ?: null,
            'success' => session('success'),
        ]);
    }}

    
    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {{"""
    for fk_meta in belongs_to_list:
        if fk_meta['column_name'] in ignore_columns:
            continue
        controller_code += f"""\n        ${fk_meta['table_name']} = {utilities.any_case_to_pascal_case(utilities.singular(fk_meta['table_name']))}::query()->orderBy('{model_utilities.get_first_text_like_column_from_table_name(connection, fk_meta['table_name'])}', 'asc')->get();"""

    controller_code += f"""


        $referrer = url()->previous();
        $route = app('router')->getRoutes()->match(request()->create($referrer));
        
        session()->put('previous_route', [
            'name' => $route->getName(),
            'params' => $route->parameters()
        ]);

        return inertia("{ln.model_class_name}/Create", ["""
    is_first = True
    for fk_meta in belongs_to_list:
        if fk_meta['column_name'] in ignore_columns:
            continue
        pre_comma = ","
        if is_first:
            pre_comma = ""

        controller_code += f"""{pre_comma}\n            '{fk_meta['table_name']}' => {utilities.any_case_to_pascal_case(utilities.singular(fk_meta['table_name']))}Resource::collection(${fk_meta['table_name']})\n"""
        is_first = False
    controller_code += f"""
        ]);
    }}

    /**
     * Store a newly created resource in storage.
     */
    public function store({ln.model_class_name}Request $request)
    {{
        $data = $request->validated();
       
        {ln.model_class_name}::create($data);
        
        $previousRoute = session()->pull('previous_route', ['name' => '{ln.lcs}.index', 'params' => []]);

        return to_route($previousRoute['name'], $previousRoute['params'])
            ->with('success', '{ln.model_class_name} was created');
    }}

    /**
     * Display the specified resource.
     */
    public function show({ln.model_class_name} ${ln.lcs})
    {{"""
    has_many_arr = []
    if len(has_many_list) > 0:
        for has_many_info in has_many_list:
            var_name = has_many_info['table_name']
            resource_name = utilities.any_case_to_pascal_case((utilities.singular(has_many_info['table_name'])))
            prop_string = f"""            '{var_name}' => {resource_name}Resource::collection(${var_name}),\n"""
            has_many_arr.append(prop_string)
            controller_code += f"""
        $query = ${ln.lcs}->{var_name}();
        ${var_name}_sortField = request("{var_name}_sort_field", 'id');
        ${var_name}_sortDirection = request("{var_name}_sort_direction", "desc");
        ${var_name} = $query->orderBy(${var_name}_sortField, ${var_name}_sortDirection)
            ->paginate(20)
            ->onEachSide(1);
            """
    belongs_to_many_arr = []
    if len(has_many_through_list) > 0:
        for belongs_to_many_info in has_many_through_list:
            var_name = utilities.join_table_name(belongs_to_many_info['table_name'], ln.tn)
            resource_name = utilities.any_case_to_pascal_case((utilities.singular(var_name)))
            prop_string = f"""            '{var_name}' => {resource_name}Resource::collection(${var_name}),\n"""
            belongs_to_many_arr.append(prop_string)
            where_string = f"""$query->where('{ln.tn}.id', ${ln.lcs}->id);\n"""
            controller_code += controller_utilities.get_show_segment_for_belongs_to_many_table_named(var_name, ignore_columns, connection, where_string)

    controller_code += f"""\n\n        $query = {ln.model_class_name}::query();\n"""
    if len(belongs_to_list) > 0:
        select_ref = []
        is_first = True
        controller_code += f"""
        $query"""
        for fk_info in belongs_to_list:
            if not is_first:
                controller_code += ' ' * 12
            controller_code += f"""->leftJoin('{fk_info['table_name']}','{fk_info['table_name']}.id', '=', '{ln.tn}.{fk_info['column_name']}')\n"""
            sql_real_ref = f"""{fk_info['table_name']}.{fk_info['view_column']}"""
            as_name = f"""{utilities.any_case_to_camel_case(fk_info['table_name']+fk_info['view_column'])}"""
            select_ref_item = f"""'{sql_real_ref} as {as_name}'"""
            select_ref.append(select_ref_item)
            is_first = False
        comma_separated_list = ", ".join(select_ref)
        controller_code += ' ' * 12  + f"""->select ('{ln.tn}.*', {comma_separated_list});\n"""
    controller_code += f"""        $query->where('{ln.tn}.id', ${ln.lcs}->id);
        ${ln.lcs}Data = $query->first();\n        
        
        
        
        return inertia("{ln.model_class_name}/Show", [
            """
    controller_code += f""""{ln.lcs}" => new {ln.model_class_name}Resource(${ln.lcs}Data),\n"""
    if len(has_many_arr) > 0:
        for has_many_string in has_many_arr:
            controller_code += has_many_string;
    if len(belongs_to_many_arr) > 0:
        for belongs_to_many_string in belongs_to_many_arr:
            controller_code += belongs_to_many_string;
    controller_code += f"""\n            'queryParams' => request()->query() ?: null\n]);
    }}

    /**
     * Show the form for editing the specified resource.
     */
    public function edit({ln.model_class_name} ${ln.lcs})
    {{
        $query = {ln.model_class_name}::query();"""
    if len(belongs_to_list) > 0:
        select_ref = []
        is_first = True
        controller_code += f"""
        $query"""
        for fk_info in belongs_to_list:
            if not is_first:
                controller_code += ' ' * 12
            controller_code += f"""->leftJoin('{fk_info['table_name']}','{fk_info['table_name']}.id', '=', '{ln.tn}.{fk_info['column_name']}')\n"""
            sql_real_ref = f"""{fk_info['table_name']}.{fk_info['view_column']}"""
            as_name = f"""{utilities.any_case_to_camel_case(fk_info['table_name']+fk_info['view_column'])}"""
            select_ref_item = f"""'{sql_real_ref} as {as_name}'"""
            select_ref.append(select_ref_item)
            is_first = False
        comma_separated_list = ", ".join(select_ref)
        controller_code += ' ' * 12  + f"""->select ('{ln.tn}.*', {comma_separated_list});"""
    controller_code += f"""
        $query->where('{ln.tn}.id', ${ln.lcs}->id);
        ${ln.lcs}Data = $query->first();
        
        $referrer = url()->previous();
        $route = app('router')->getRoutes()->match(request()->create($referrer));
        
        session()->put('previous_route', [
            'name' => $route->getName(),
            'params' => $route->parameters()
        ]);
"""
    for fk_meta in belongs_to_list:
        if fk_meta['column_name'] in ignore_columns:
            continue
        controller_code += f"""\n        ${fk_meta['table_name']} = {utilities.any_case_to_pascal_case(utilities.singular(fk_meta['table_name']))}::query()->orderBy('{model_utilities.get_first_text_like_column_from_table_name(connection, fk_meta['table_name'])}', 'asc')->get();"""

    controller_code += f"""

        return inertia("{ln.model_class_name}/Edit", [
            "{ln.lcs}" => new {ln.model_class_name}Resource(${ln.lcs}Data),\n"""

    for fk_meta in belongs_to_list:
        if fk_meta['column_name'] in ignore_columns:
            continue

        controller_code += f"""           '{fk_meta['table_name']}' => {utilities.any_case_to_pascal_case(utilities.singular(fk_meta['table_name']))}Resource::collection(${fk_meta['table_name']}),\n"""
        is_first = False
    controller_code += f"""        ]);
    }}

    /**
     * Update the specified resource in storage.
     */
    public function update({ln.model_class_name}Request $request, {ln.model_class_name} ${ln.lcs})
    {{
        $data = $request->validated();
        ${ln.lcs}->update($data);

        $previousRoute = session()->pull('previous_route', ['name' => 'location.index', 'params' => []]);

        return to_route($previousRoute['name'], $previousRoute['params'])
            ->with('success', "{ln.model_class_name} \\"${ln.lcs}->{utilities.any_case_to_title( utilities.get_first_textlike_column(columns, ignore_columns))}\\" was updated");
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
        $referrer = url()->previous();
        $route = app('router')->getRoutes()->match(request()->create($referrer));

        return to_route($route->getName(), $route->parameters())
            ->with('success', "{ln.model_class_name} \\"$name\\" was deleted");
    }}
}}
    """
    return controller_code
