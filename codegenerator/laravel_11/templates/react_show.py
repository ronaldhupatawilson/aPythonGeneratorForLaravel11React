from codegenerator.laravel_11 import utilities
from codegenerator.laravel_11 import react_show_utilities


def get_show_code(ln, ci, columns, ignore_columns, belongs_to_list, has_many_list, has_many_through_list, connection):
    code = f"""import React from 'react';
import {{ Head, Link }} from '@inertiajs/react';
import {{ 
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

{react_show_utilities.get_own_interface(columns, ignore_columns, belongs_to_list, ln)}

{react_show_utilities.get_props_interface(ln)}

export default function Create({{ auth, {ln.lcs} }}: Props) {{

  return (
    <AuthenticatedLayout
      user={{auth.user}}
      header={{
        <Box className="flex justify-between items-center">
          <Typography variant="h6" className="text-gray-800 dark:text-gray-200">
            {ln.model_class_name} : {{ {ln.lcs}.{utilities.get_first_textlike_column(columns, ignore_columns)} }}
          </Typography>
        </Box>
      }}
    >
      <Head title={{`{ln.cfp} : ${{ {ln.lcs}.{utilities.get_first_textlike_column(columns, ignore_columns)} }}`}} />

      <Container className="py-12">
        <Paper className="p-4 sm:p-8 bg-white dark:bg-gray-800 shadow sm:rounded-lg">
{react_show_utilities.get_display_fields(columns, ignore_columns, belongs_to_list, connection, ln)}          

        </Paper>
      </Container>
    </AuthenticatedLayout>
  );
}}"""
    return code
