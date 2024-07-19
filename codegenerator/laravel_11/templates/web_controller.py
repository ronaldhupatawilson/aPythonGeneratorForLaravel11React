# ln=laravel names, ci= column info
def get_web_controller_file_content(ln, ci, belongs_to_list, has_many_list, has_many_through_list):
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
        $query = {ln.model_class_name}::query();

        $sortField = request("sort_field", 'created_at');
        $sortDirection = request("sort_direction", "desc");

        if (request("name")) {{
            $query->where("name", "like", "%" . request("name") . "%");
        }}
        if (request("status")) {{
            $query->where("status", request("status"));
        }}

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
        /** @var $image \Illuminate\Http\UploadedFile */
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
            ->with('success', "{ln.model_class_name} \"${ln.lcs}->name\" was updated");
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
            ->with('success', "{ln.model_class_name} \"$name\" was deleted");
    }}
}}
    """
    return controller_code
