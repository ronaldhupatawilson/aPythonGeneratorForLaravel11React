from codegenerator.laravel_11 import react_create_utilities


def get_create_code(ln, ci, columns, ignore_columns, belongs_to_list, has_many_list, has_many_through_list, connection):
    code = f"""import React from 'react';
import {{ useForm, Head, Link }} from '@inertiajs/react';
import {{ 
  TextField, 
  Button, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Typography,
  Box,
  Container,
  Paper
}} from '@mui/material';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';


export interface User {{
    id: number;
    name: string;
    email: string;
    email_verified_at: string;
}}

export interface Auth {{
    user: User;
}}

interface FormData {{
{react_create_utilities.get_formdata_interface(columns, ignore_columns)}
}}

{react_create_utilities.get_foreign_key_interfaces(columns, ignore_columns, belongs_to_list)}

{react_create_utilities.get_props_interface(columns, ignore_columns, belongs_to_list)}

export default function Create({{ {react_create_utilities.get_props_interfaces_as_csl( ignore_columns, belongs_to_list)} }}: Props) {{
  const {{ data, setData, post, errors }} = useForm<FormData>({{
    {react_create_utilities.get_props(columns, ignore_columns)}
  }});

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {{
    e.preventDefault();
    post(route('{ln.lcs}.store'));
  }};

  return (
    <AuthenticatedLayout
      user={{auth.user}}
      header={{
        <Box className="flex justify-between items-center">
          <Typography variant="h6" className="text-gray-800 dark:text-gray-200">
            Create a new {ln.model_class_name}
          </Typography>
        </Box>
      }}
    >
      <Head title="{ln.cfp}" />

      <Container className="py-12">
        <Paper className="p-4 sm:p-8 bg-white dark:bg-gray-800 shadow sm:rounded-lg">
          <form onSubmit={{onSubmit}}>
            <div className="grid grid-gap-4">
{react_create_utilities.get_create_form_fields(columns, ignore_columns, belongs_to_list, connection)}          
           </div>

            <Box className="mt-4 text-right">
              <Link
                href={{route('{ln.lcs}.index')}}
                className="bg-gray-100 py-2 px-4 text-gray-800 rounded shadow transition-all hover:bg-gray-200 mr-2"
              >
                Cancel
              </Link>
              <Button type="submit" variant="contained" color="primary">
                Submit
              </Button>
            </Box>
          </form>
        </Paper>
      </Container>
    </AuthenticatedLayout>
  );
}}"""
    return code
