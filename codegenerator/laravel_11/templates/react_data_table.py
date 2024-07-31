from codegenerator.laravel_11 import utilities
from codegenerator.laravel_11 import react_data_table_utilities

def get_data_table_code(ln, ci, columns, ignore_columns, belongs_to_list, has_many_list, has_many_through_list, connection):
    code = f"""import React from 'react';
import {{ Head, Link, router }} from '@inertiajs/react';
import {{ 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Paper,
  TextField,
  Select,
  MenuItem,
  Button,
  Typography,
  Box,
  Container,
  Alert
}} from '@mui/material';
import Pagination from '@/Components/Pagination';
import TableHeading from '@/Components/TableHeading';

interface User {{
    id: number;
    name: string;
    email: string;
}}

interface PaginationLinks {{
    url: string | null;
    label: string;
    active: boolean;
}}


interface {ln.model_class_name} {{
{ ci.typescript_interface_fields }
}}

interface IndexProps {{
  auth: {{
    user: User;
  }};
  {ln.tn}: {{
    data: {ln.cfs}[];
    meta: {{
      links: PaginationLinks[];
    }};
  }};
  queryParams?: Record<string, string> | null;
  success?: string;
}}

export default function Index({{ auth, {ln.tn}, queryParams = {{}}, success }}: IndexProps) {{
 
  
    const defaultQueryParams = {{
        sort_field: "id",
        sort_direction: "asc",
    }};

    // Merge the provided queryParams (if any) with the default values
    const mergedQueryParams = {{
        ...defaultQueryParams,
        ...(queryParams || {{}}),
    }};

   const searchFieldChanged = (name: string, value: string) => {{
    const newQueryParams = {{ ...mergedQueryParams }};
    if (value) {{
      newQueryParams[name] = value;
    }} else {{
      delete newQueryParams[name];
    }}
    router.get(route('{ln.lcs}.index'), newQueryParams);
  }};

  const onKeyPress = (
     name: string, 
     e: React.KeyboardEvent<HTMLInputElement>
     ) => {{
    if (e.key !== 'Enter') return;
    searchFieldChanged(name, (e.target as HTMLInputElement).value);
  }};

  const sortChanged = (name: string) => {{
        const newQueryParams = {{ ...mergedQueryParams }};
    if (name === newQueryParams.sort_field) {{
      newQueryParams.sort_direction = newQueryParams.sort_direction === 'asc' ? 'desc' : 'asc';
    }} else {{
      newQueryParams.sort_field = name;
      newQueryParams.sort_direction = 'asc';
    }}
    router.get(route('{ln.lcs}.index'), newQueryParams);
  }};

  const delete{ln.cfs} = ({ln.lcs}: {ln.cfs}) => {{
    if (!window.confirm('Are you sure you want to delete the {ln.lcs}?')) {{
      return;
    }}
    router.delete(route('{ln.lcs}.destroy', {ln.lcs}.id));
  }};

  return (
    <div className="mt-5">
      <Head title="{utilities.any_case_to_title(ln.tn)}" />

      <Container className="py-12">
        {{success && (
          <Alert severity="success" className="mb-4">
            {{success}}
          </Alert>
        )}}
        <Paper className="overflow-hidden shadow-sm sm:rounded-lg">
        <Box className="flex justify-between items-center p-2">
          <Typography variant="h6" className="text-gray-800 dark:text-gray-200">
            {ln.title}
          </Typography>
          <Link
            href={{route('{ln.lcs}.create')}}
            className="bg-lime-400 py-1 px-3 text-black hover:text-white rounded shadow transition-all hover:bg-lime-800"
          >
            Add new
          </Link>
        </Box>
          <Box className="p-6 text-gray-900 dark:text-gray-100">
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
{react_data_table_utilities.get_react_index_table_headings(columns, ignore_columns, belongs_to_list)}
                    <th>&nbsp;</th>
                  </TableRow>
                </TableHead>
                
                <TableHead>
                  <TableRow>
{react_data_table_utilities.get_react_index_table_search_headings(columns, ignore_columns, belongs_to_list)}
                    <TableCell></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {{{ln.tn}.data.map(({ln.tns}) => (
                    <TableRow key={{{ln.tns}.id}} 
                                            className={{`even:bg-gray-100 dark:even:bg-gray-800
                                            hover:bg-lime-200 hover:text-white
                                            cursor-pointer transition-colors duration-150 ease-in-out
                                        `}}
                                            onClick={{() =>
                                                (window.location.href = route(
                                                    "{ln.tns}.show",
                                                    {ln.tns}.id
                                                ))
                                            }}>
{react_data_table_utilities.react_index_table_data_cells(ci.columns, ci.ignore_columns, ln.tns, belongs_to_list, connection)}                    
                      <TableCell align="right">
                       <div className="flex justify-between items-center">
                       <div>
                        <Link
                          href={{route('{ln.lcs}.edit', {ln.tns}.id)}}
                          className="font-medium text-gray-500 hover:text-blue-600 dark:text-blue-500 hover:underline mx-5"
                          onClick={{(e) => e.stopPropagation()}}
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" class="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
</svg>

                        </Link>
                        </div><div>
                        
                        <button
                          onClick={{(e) => {{ e.stopPropagation(); delete{ln.cfs}({ln.tns}) }} }}
                          className="font-medium text-gray-500 hover:text-red-600"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" class="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
</svg>

                        </button>
                        </div></div>
                      </TableCell>
                    </TableRow>
                  ))}}
                </TableBody>
              </Table>
            </TableContainer>
            <Pagination links={{{ln.tn}.meta.links}} />
          </Box>
        </Paper>
      </Container>
    </div>
  );
}}
"""
    return code
