# ln=laravel names, ci= column info
def get_web_routes_authentication_setup():
    code = f"""<?php
Route::get('/setup', function () {{
    $credentials = [
        'email' => 'admin@admin.com',
        'password' => 'password'
    ];

    if(!Auth::attempt($credentials))
    {{
        $user = new \\App\\Models\\User();
        
        $user->name = 'Admin';
        $user->email = $credentials['email'];
        $user->password = Hash::make($credentials['password']);
        $user->save();

        if(Auth::attempt($credentials))
        {{
            $user = Auth::user();

            $adminToken = $user->createToken('admin-token',['*']);
            $updateToken = $user->createToken('update-token',['create','update']);
            $basicToken = $user->createToken('basic-token',['read']);

            return response()->json([
                'admin' => $adminToken->plainTextToken,
                'update' => $updateToken->plainTextToken,
                'basic' => $basicToken->plainTextToken,
            ]);

        }}

    }}

}});
    """
    return code

