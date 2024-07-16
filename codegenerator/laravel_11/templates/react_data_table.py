# ln=laravel names, ci= column info
def get_react_component_data_table_content(ln, ci):
    code = f"""<template>
  <div>
    <table class="w-full">
      <thead>
        <tr>
          <th>Question Type</th>
          <th>Old Code</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="questionType in questionTypes" :key="questionType.id">
          <td>{{{{ questionType.questionType }}}}</td>
          <td>{{{{ questionType.oldCode }}}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {{ defineComponent }} from 'vue';

export default defineComponent({{
  name: 'QuestionTypes',

  props: {{
    questionTypes: {{
      type: Array,
      required: true,
    }},
  }},
}});
</script>

<style>
table {{
  border-collapse: collapse;
  width: 100%;
}}

th,
td {{
  padding: 10px;
  text-align: center;
}}
</style>
"""
    return code
