# ln=laravel names, ci= column info
def get_policy_file_content(ln, ci):
    code = f"""<?php

namespace App\Policies;

use App\\Models\\{ln.model_class_name};
use App\\Models\\User;
use Illuminate\\Auth\\Access\\Response;

class {ln.policy_class_name}
{{
    /**
     * Determine whether the user can view any models.
     */
    public function viewAny(User $user): bool
    {{
        if ($user->hasRole('admin')) {{
            return true;
        }}
        
        return false;
        
    }}

    /**
     * Determine whether the user can view the model.
     */
    public function view(User $user, {ln.model_class_name} ${ln.lower_case_model_class_name}): bool
    {{
        return $user->id === ${ln.lower_case_model_class_name}->user_id;
    }}

    /**
     * Determine whether the user can create models.
     */
    public function create(User $user): bool
    {{
        return $user->id === ${ln.lower_case_model_class_name}->user_id;
    }}

    /**
     * Determine whether the user can update the model.
     */
    public function update(User $user, {ln.model_class_name} ${ln.lower_case_model_class_name}): bool
    {{
        return $user->id === ${ln.lower_case_model_class_name}->user_id;
    }}

    /**
     * Determine whether the user can delete the model.
     */
    public function delete(User $user, {ln.model_class_name} ${ln.lower_case_model_class_name}): bool
    {{
        return $user->id === ${ln.lower_case_model_class_name}->user_id;
    }}

    /**
     * Determine whether the user can restore the model.
     */
    public function restore(User $user, {ln.model_class_name} ${ln.lower_case_model_class_name}): bool
    {{
        //return $user->id === ${ln.lower_case_model_class_name}->user_id;
    }}

    /**
     * Determine whether the user can permanently delete the model.
     */
    public function forceDelete(User $user, {ln.model_class_name} ${ln.lower_case_model_class_name}): bool
    {{
        //return $user->id === ${ln.lower_case_model_class_name}->user_id;
    }}
}}

    """
    return code
