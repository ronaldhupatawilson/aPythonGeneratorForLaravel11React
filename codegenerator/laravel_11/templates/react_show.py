from codegenerator.laravel_11 import utilities
from codegenerator.laravel_11 import react_show_utilities

def get_show_code(ln, ci, columns, ignore_columns, belongs_to_list, has_many_list, belongs_to_many_list, connection):
    code = f"""import React from 'react';
import {{ Head, Link }} from '@inertiajs/react';
import {{ Typography, Box, Container, Paper }} from '@mui/material';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
"""
    comma_separated_has_many_list = ""
    query_params_interface_string = ""
    props_has_many_string = ""
    included_components = ""
    has_many_interfaces = ""
    if len(has_many_list) > 0:
        for has_many in has_many_list:
            code += f"""import {utilities.any_case_to_pascal_case(utilities.singular(has_many['table_name']))} from "../{utilities.any_case_to_pascal_case(utilities.singular(has_many['table_name']))}/DataTable"; \n"""
            comma_separated_has_many_list += f"""{has_many['table_name']}, """
            query_params_interface_string += f"""    {has_many['table_name']}_sort_fields: string;\n    {has_many['table_name']}_sort_direction: string ;\n"""
            props_has_many_string += f"""    {has_many['table_name']}: {utilities.lower_case_single(has_many['table_name'])}[];\n"""
            included_components += f"""                <Paper className="p-4 mt-5 sm:p-8 bg-white dark:bg-gray-800 shadow sm:rounded-lg">
                    <{utilities.any_case_to_pascal_case(utilities.singular(has_many['table_name']))}
                        auth={{auth}}
                        {has_many['table_name']}={{ {has_many['table_name']} }}
                        queryParams={{queryParams}}
                        success={{success}}
                    />
                </Paper>\n"""
            has_many_interfaces += utilities.get_interface_info_from_table_name(connection, has_many['table_name'], ignore_columns)

    comma_separated_belongs_to_many_list = ""
    btm_query_params_interface_string = ""
    props_belongs_to_many_string = ""
    btm_included_components = ""
    belongs_to_many_interfaces = ""
    if len(belongs_to_many_list) > 0:
        for belongs_to_many in belongs_to_many_list:
            code += f"""import {utilities.any_case_to_pascal_case(utilities.singular(belongs_to_many['table_name']))} from "../{utilities.any_case_to_pascal_case(utilities.singular(belongs_to_many['table_name']))}/DataTable"; \n"""
            comma_separated_belongs_to_many_list += f"""{belongs_to_many['table_name']}, """
            btm_query_params_interface_string += f"""    {belongs_to_many['table_name']}_sort_fields: string;\n    {belongs_to_many['table_name']}_sort_direction: string ;\n"""
            props_belongs_to_many_string += f"""    {belongs_to_many['table_name']}: {utilities.lower_case_single(belongs_to_many['table_name'])}[];\n"""
            btm_included_components += f"""                <Paper className="p-4 mt-5 sm:p-8 bg-white dark:bg-gray-800 shadow sm:rounded-lg">
                    <{utilities.any_case_to_pascal_case(utilities.singular(belongs_to_many['table_name']))}
                        auth={{auth}}
                        {belongs_to_many['table_name']}={{ {belongs_to_many['table_name']} }}
                        queryParams={{queryParams}}
                        success={{success}}
                    />
                </Paper>\n"""
            belongs_to_many_interfaces += utilities.get_interface_info_from_table_name(connection, belongs_to_many['table_name'], ignore_columns)
    code += f"""
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

{has_many_interfaces}

{belongs_to_many_interfaces}

interface QueryParams {{
    sort_field: string;
    sort_direction: string;
{query_params_interface_string}
{btm_query_params_interface_string}
}}

interface Props {{
    auth: Auth;
    {ln.lcs}: {ln.lcs};
{props_has_many_string} {props_belongs_to_many_string}    queryParams: QueryParams | null;
    success: string;
}}


export default function Create({{ auth, {ln.lcs}, {comma_separated_has_many_list}{comma_separated_belongs_to_many_list}queryParams, success }}: Props) {{
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
{included_components}

{btm_included_components}
      </Container>
    </AuthenticatedLayout>
  );
}}"""
    return code
