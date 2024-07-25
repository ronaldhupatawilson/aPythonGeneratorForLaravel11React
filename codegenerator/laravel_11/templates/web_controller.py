from codegenerator.laravel_11 import utilities
from codegenerator.laravel_11 import model_utilities

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
        controller_code += f"use App\\Http\\Requests\\{utilities.model_class_name_from_table_name(item['table_name'])}Request;\n"
        controller_code += f"use App\\Http\\Resources\\{utilities.model_class_name_from_table_name(item['table_name'])}Resource;\n"

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
            ->paginate(10)
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

        return to_route('{ln.lcs}.index')
            ->with('success', '{ln.model_class_name} was created');
    }}

    /**
     * Display the specified resource.
     */
    public function show({ln.model_class_name} ${ln.lcs})
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

        return inertia("{ln.model_class_name}/Show", [
            "{ln.lcs}" => new {ln.model_class_name}Resource(${ln.lcs}Data),\n"""
    controller_code += f"""        ]);
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
        ${ln.lcs}Data = $query->first();"""
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

        return to_route('{ln.lcs}.index')
            ->with('success', "{ln.model_class_name} \\"${ln.lcs}->{utilities.get_first_textlike_column(columns, ignore_columns)}\\" was updated");
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
