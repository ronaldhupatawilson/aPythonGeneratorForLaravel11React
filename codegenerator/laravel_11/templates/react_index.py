from codegenerator.laravel_11.utilities import react_index_table_data_cells

def get_index_code(ln, ci, belongs_to_list, has_many_list, has_many_through_list):
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
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
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
  {ln.lctn}: {{
    data: {ln.cfs}[];
    meta: {{
      links: PaginationLinks[];
    }};
  }};
  queryParams?: Record<string, string> | null;
  success?: string;
}}

export default function Index({{ auth, {ln.lctn}, queryParams = {{}}, success }}: IndexProps) {{
 
  
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
    <AuthenticatedLayout
      user={{auth.user}}
      header={{
        <Box className="flex justify-between items-center">
          <Typography variant="h6" className="text-gray-800 dark:text-gray-200">
            {ln.title}
          </Typography>
          <Link
            href={{route('{ln.lcs}.create')}}
            className="bg-emerald-500 py-1 px-3 text-white rounded shadow transition-all hover:bg-emerald-600"
          >
            Add new
          </Link>
        </Box>
      }}
    >
      <Head title="{ln.cfp}" />

      <Container className="py-12">
        {{success && (
          <Alert severity="success" className="mb-4">
            {{success}}
          </Alert>
        )}}
        <Paper className="overflow-hidden shadow-sm sm:rounded-lg">
          <Box className="p-6 text-gray-900 dark:text-gray-100">
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
{ci.react_index_table_headings}
                    <th align="right">Actions</th>
                  </TableRow>
                </TableHead>
                
                <TableHead>
                  <TableRow>
{ci.react_index_table_search_headings}
                    <TableCell></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {{{ln.lctn}.data.map(({ln.lcs}) => (
                    <TableRow key={{{ln.lcs}.id}}>
{react_index_table_data_cells(ci.columns, ci.ignore_columns, ln.lcs)}                    
                      <TableCell align="right">
                        <Link
                          href={{route('{ln.lcs}.edit', {ln.lcs}.id)}}
                          className="font-medium text-blue-600 dark:text-blue-500 hover:underline mx-1"
                        >
                          Edit
                        </Link>
                        <Button
                          onClick={{() => delete{ln.cfs}({ln.lcs})}}
                          className="font-medium text-red-600 dark:text-red-500 hover:underline mx-1"
                        >
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}}
                </TableBody>
              </Table>
            </TableContainer>
            <Pagination links={{{ln.lctn}.meta.links}} />
          </Box>
        </Paper>
      </Container>
    </AuthenticatedLayout>
  );
}}
"""
    return code
