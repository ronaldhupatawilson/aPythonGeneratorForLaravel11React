# ln=laravel names, ci= column info
def get_unit_test_file_content(ln, ci):
    controller_test_code = f"""<?php

namespace Tests\\Unit;

use App\\Models\\{ln.cfs};
use App\\Models\\User;
use Illuminate\\Http\\Response;
use Tests\\TestCase;

class {ln.test_unit_class_name} extends TestCase
{{
    public function test_it_requires_authentication()
    {{
        ${ln.lcs} = {ln.cfs}::factory()->create();

        $this->getJson('/api/{ln.lcp}')
            ->assertUnauthorized();

        $this->postJson('/api/{ln.lcp}', [
            {ci.column_test_fields_fillable_as_associative_array}
        ])->assertUnauthorized();

        $this->getJson("/api/{ln.lcp}/{{${ln.lcs}->id}}")
            ->assertUnauthorized();

        $this->patchJson("/api/{ln.lcp}/{{${ln.lcs}->id}}", [
            {ci.column_test_fields_fillable_as_associative_array}
        ])->assertUnauthorized();
    }}

    public function test_it_stores_a_{ln.lcs}()
    {{
        $user = User::factory()->create();

        $response = $this
            ->actingAs($user)
            ->postJson('/api/{ln.lcp}', [
                {ci.column_test_fields_fillable_as_associative_array}
            ]);

        $response
            ->assertCreated()
            ->assertExactJson([
                'data' => [
                    {ci.column_test_fields_fillable_as_associative_array}
                ],
        ]);
    }}

    public function test_it_shows_a_{ln.lcs}()
    {{
        $user = User::factory()->create();
        ${ln.lcs} = {ln.cfs}::factory()->create();

        $response = $this
            ->actingAs($user)
            ->getJson("/api/{ln.lcp}/{{${ln.lcs}->id}}");

        $response
            ->assertOk()
            ->assertJson([
                'data' => [
                    'first_name' => ${ln.lcs}->first_name,
                    'last_name' => ${ln.lcs}->last_name,
                    'date_of_birth' => ${ln.lcs}->date_of_birth->format('Y-m-d'),
                    'email' => ${ln.lcs}->email,
                ],
            ]);
    }}

    public function test_it_indexes_{ln.lcp}()
    {{
        $user = User::factory()->create();
        {ln.cfs}::factory()->times(3)->create();

        $response = $this
            ->actingAs($user)
            ->getJson('/api/{ln.lcp}');

        $response
            ->assertOk()
            ->assertJsonCount(3, 'data')
            ->assertJsonStructure([
                'data' => [
                    [
                        {ci.comma_separated_list_of_column_names}
                    ]
                ]
            ]);
    }}

    public function test_it_updates_a_{ln.lcs}()
    {{
        $user = User::factory()->create();
        ${ln.lcs} = {ln.cfs}::factory()->create([
            '{ci.first_nullable_textlike_column}' => null,
        ]);

        $response = $this
            ->actingAs($user)
            ->patchJson("/api/{ln.lcp}/{{${ln.lcs}->id}}", [
                '{ci.first_nullable_textlike_column}' => 'sarah.connor@example.com',
            ]);

        $response
            ->assertOk()
            ->assertJson([
                'data' => [
                    {ci.column_test_fields_fillable_as_associative_array}
                ],
            ]);
    }}

    public function test_it_prevents_emptying_fields()
    {{
        $user = User::factory()->create();
        ${ln.lcs} = {ln.cfs}::factory()->create();

        $response = $this
            ->actingAs($user)
            ->patchJson("/api/{ln.lcp}/{{${ln.lcs}->id}}", [
                '{ci.first_non_null_column}' => '',
            ]);

        $response
            ->assertStatus(Response::HTTP_UNPROCESSABLE_ENTITY)
            ->assertJsonValidationErrors('{ci.first_non_null_column}');
    }}

    public function test_it_prevents_deleting_{ln.lcp}()
    {{
        $user = User::factory()->create();
        ${ln.lcs} = {ln.cfs}::factory()->create();

        $response = $this
            ->actingAs($user)
            ->deleteJson("/api/{ln.lcp}/{{${ln.lcs}->id}}");

        $response
            ->assertStatus(Response::HTTP_METHOD_NOT_ALLOWED);
    }}
}}
    """

    return controller_test_code
