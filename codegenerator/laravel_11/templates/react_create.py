# ln=laravel names, ci= column info
def get_react_component_create_content(ln, ci):
    code = f"""<template>
  <div>
    <form v-if="mode === 'add'">
      <div class="mb-4">
        <label for="questionType">Question Type</label>
        <input type="text" id="questionType" v-model="questionType" class="w-full form-control" />
        <div class="invalid-feedback" v-if="errors.questionType">
          {{{{ errors.questionType }}}}
        </div>
      </div>
      <div class="mb-4">
        <label for="oldCode">Old Code</label>
        <input type="text" id="oldCode" v-model="oldCode" class="w-full form-control" />
        <div class="invalid-feedback" v-if="errors.oldCode">
          {{{{ errors.oldCode }}}}
        </div>
      </div>
      <button class="btn btn-primary" @click="addQuestionType">Add Question Type</button>
    </form>
    <form v-if="mode === 'edit'">
      <div class="mb-4">
        <label for="questionType">Question Type</label>
        <input type="text" id="questionType" v-model="questionType" class="w-full form-control" />
        <div class="invalid-feedback" v-if="errors.questionType">
          {{{{ errors.questionType }}}}
        </div>
      </div>
      <div class="mb-4">
        <label for="oldCode">Old Code</label>
        <input type="text" id="oldCode" v-model="oldCode" class="w-full form-control" />
        <div class="invalid-feedback" v-if="errors.oldCode">
          {{{{ errors.oldCode }}}}
        </div>
      </div>
      <button class="btn btn-primary" @click="updateQuestionType">Update Question Type</button>
    </form>
    <div class="form-text text-gray-500">
      <i class="far fa-info-circle" />
      Hover over a label to see a help message.
    </div>
  </div>
</template>

<script>
import {{ defineComponent, ref }} from 'vue';
import {{ usePage }} from '@inertiajs/vue';

export default defineComponent({{
  name: 'QuestionTypeForm',

  props: {{
    mode: {{
      type: String,
      required: true,
    }},
  }},

  setup() {{
    const questionType = ref('');
    const oldCode = ref('');
    const errors = ref({{}});

    const {{ route }} = usePage();

    const addQuestionType = () => {{
      route.post('/question-types', {{
        questionType: questionType.value,
        oldCode: oldCode.value,
      }}).then(() => {{
        errors.value = {{}};
      }});
    }};

    const updateQuestionType = () => {{
      route.put('/question-types/' + questionType.value, {{
        questionType: questionType.value,
        oldCode: oldCode.value,
      }}).then(() => {{
        errors.value = {{}};
      }});
    }};

    return {{
      questionType,
      oldCode,
      errors,
      addQuestionType,
      updateQuestionType,
    }};
  }},
}});
</script>

<style>
form {{
  width: 500px;
}}

.invalid-feedback {{
  color: red;
}}

.form-text {{
  font-size: 14px;
  margin-top: 10px;
}}

.far {{
  cursor: pointer;
}}
</style>"""
    return code
