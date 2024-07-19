# ln=laravel names, ci= column info
def get_index_code(ln, ci, belongs_to_list, has_many_list, has_many_through_list):
    code = f"""
import React from 'react';
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
import {{ PROJECT_STATUS_CLASS_MAP, PROJECT_STATUS_TEXT_MAP }} from '@/constants';

interface Project {{
  id: number;
  name: string;
  status: string;
  created_at: string;
  due_date: string;
  image_path: string;
  createdBy: {{
    name: string;
  }};
}}

interface IndexProps {{
  auth: {{
    user: any;
  }};
  projects: {{
    data: Project[];
    meta: {{
      links: any[];
    }};
  }};
  queryParams?: Record<string, string>;
  success?: string;
}}

export default function Index({{ auth, projects, queryParams = {{}}, success }}: IndexProps) {{
  const searchFieldChanged = (name: string, value: string) => {{
    if (value) {{
      queryParams[name] = value;
    }} else {{
      delete queryParams[name];
    }}
    router.get(route('project.index'), queryParams);
  }};

  const onKeyPress = (name: string, e: React.KeyboardEvent<HTMLInputElement>) => {{
    if (e.key !== 'Enter') return;
    searchFieldChanged(name, (e.target as HTMLInputElement).value);
  }};

  const sortChanged = (name: string) => {{
    if (name === queryParams.sort_field) {{
      queryParams.sort_direction = queryParams.sort_direction === 'asc' ? 'desc' : 'asc';
    }} else {{
      queryParams.sort_field = name;
      queryParams.sort_direction = 'asc';
    }}
    router.get(route('project.index'), queryParams);
  }};

  const deleteProject = (project: Project) => {{
    if (!window.confirm('Are you sure you want to delete the project?')) {{
      return;
    }}
    router.delete(route('project.destroy', project.id));
  }};

  return (
    <AuthenticatedLayout
      user={{auth.user}}
      header={{
        <Box className="flex justify-between items-center">
          <Typography variant="h6" className="text-gray-800 dark:text-gray-200">
            Projects
          </Typography>
          <Link
            href={{route('project.create')}}
            className="bg-emerald-500 py-1 px-3 text-white rounded shadow transition-all hover:bg-emerald-600"
          >
            Add new
          </Link>
        </Box>
      }}
    >
      <Head title="Projects" />

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
                    <TableHeading
                      name="id"
                      sort_field={{queryParams.sort_field}}
                      sort_direction={{queryParams.sort_direction}}
                      sortChanged={{sortChanged}}
                    >
                      ID
                    </TableHeading>
                    <TableCell>Image</TableCell>
                    <TableHeading
                      name="name"
                      sort_field={{queryParams.sort_field}}
                      sort_direction={{queryParams.sort_direction}}
                      sortChanged={{sortChanged}}
                    >
                      Name
                    </TableHeading>
                    <TableHeading
                      name="status"
                      sort_field={{queryParams.sort_field}}
                      sort_direction={{queryParams.sort_direction}}
                      sortChanged={{sortChanged}}
                    >
                      Status
                    </TableHeading>
                    <TableHeading
                      name="created_at"
                      sort_field={{queryParams.sort_field}}
                      sort_direction={{queryParams.sort_direction}}
                      sortChanged={{sortChanged}}
                    >
                      Create Date
                    </TableHeading>
                    <TableHeading
                      name="due_date"
                      sort_field={{queryParams.sort_field}}
                      sort_direction={{queryParams.sort_direction}}
                      sortChanged={{sortChanged}}
                    >
                      Due Date
                    </TableHeading>
                    <TableCell>Created By</TableCell>
                    <TableCell align="right">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableHead>
                  <TableRow>
                    <TableCell></TableCell>
                    <TableCell></TableCell>
                    <TableCell>
                      <TextField
                        fullWidth
                        defaultValue={{queryParams.name}}
                        placeholder="Project Name"
                        onBlur={{(e) => searchFieldChanged('name', e.target.value)}}
                        onKeyPress={{(e) => onKeyPress('name', e)}}
                      />
                    </TableCell>
                    <TableCell>
                      <Select
                        fullWidth
                        defaultValue={{queryParams.status}}
                        onChange={{(e) => searchFieldChanged('status', e.target.value)}}
                      >
                        <MenuItem value="">Select Status</MenuItem>
                        <MenuItem value="pending">Pending</MenuItem>
                        <MenuItem value="in_progress">In Progress</MenuItem>
                        <MenuItem value="completed">Completed</MenuItem>
                      </Select>
                    </TableCell>
                    <TableCell></TableCell>
                    <TableCell></TableCell>
                    <TableCell></TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {{projects.data.map((project) => (
                    <TableRow key={{project.id}}>
                      <TableCell>{{project.id}}</TableCell>
                      <TableCell>
                        <img src={{project.image_path}} style={{{{ width: 60 }}}} alt={{project.name}} />
                      </TableCell>
                      <TableCell>
                        <Link href={{route('project.show', project.id)}} className="text-blue-600 hover:underline">
                          {{project.name}}
                        </Link>
                      </TableCell>
                      <TableCell>
                        <span className={{`px-2 py-1 rounded text-white ${{PROJECT_STATUS_CLASS_MAP[project.status]}}`}}>
                          {{PROJECT_STATUS_TEXT_MAP[project.status]}}
                        </span>
                      </TableCell>
                      <TableCell>{{project.created_at}}</TableCell>
                      <TableCell>{{project.due_date}}</TableCell>
                      <TableCell>{{project.createdBy.name}}</TableCell>
                      <TableCell align="right">
                        <Link
                          href={{route('project.edit', project.id)}}
                          className="font-medium text-blue-600 dark:text-blue-500 hover:underline mx-1"
                        >
                          Edit
                        </Link>
                        <Button
                          onClick={{() => deleteProject(project)}}
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
            <Pagination links={{projects.meta.links}} />
          </Box>
        </Paper>
      </Container>
    </AuthenticatedLayout>
  );
}}
"""
    return code
