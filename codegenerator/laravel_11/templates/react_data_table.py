# ln=laravel names, ci= column info
def get_data_table_code(ln, ci, belongs_to_list, has_many_list, has_many_through_list):
    code = f"""import React from 'react';
import {{ Link, router }} from '@inertiajs/react';
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
  Alert
}} from '@mui/material';
import Pagination from '@/Components/Pagination';
import TableHeading from '@/Components/TableHeading';
import {{ TASK_STATUS_CLASS_MAP, TASK_STATUS_TEXT_MAP }} from '@/constants';

interface Task {{
  id: number;
  name: string;
  status: string;
  created_at: string;
  due_date: string;
  image_path: string;
  createdBy: {{
    name: string;
  }};
  project?: {{
    name: string;
  }};
}}

interface TasksTableProps {{
  tasks: {{
    data: Task[];
    meta: {{
      links: any[];
    }};
  }};
  success?: string;
  queryParams?: Record<string, string>;
  hideProjectColumn?: boolean;
}}

export default function TasksTable({{ tasks, success, queryParams = {{}}, hideProjectColumn = false }}: TasksTableProps) {{
  const searchFieldChanged = (name: string, value: string) => {{
    if (value) {{
      queryParams[name] = value;
    }} else {{
      delete queryParams[name];
    }}
    router.get(route('task.index'), queryParams);
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
    router.get(route('task.index'), queryParams);
  }};

  const deleteTask = (task: Task) => {{
    if (!window.confirm('Are you sure you want to delete the task?')) {{
      return;
    }}
    router.delete(route('task.destroy', task.id));
  }};

  return (
    <Box>
      {{success && (
        <Alert severity="success" className="mb-4">
          {{success}}
        </Alert>
      )}}
      <TableContainer component={{Paper}}>
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
              {{!hideProjectColumn && <TableCell>Project Name</TableCell>}}
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
              {{!hideProjectColumn && <TableCell></TableCell>}}
              <TableCell>
                <TextField
                  fullWidth
                  defaultValue={{queryParams.name}}
                  placeholder="Task Name"
                  onBlur={{(e) => searchFieldChanged('name', e.target.value)}}
                  onKeyPress={{(e) => onKeyPress('name', e)}}
                />
              </TableCell>
              <TableCell>
                <Select
                  fullWidth
                  defaultValue={{queryParams.status}}
                  onChange={{(e) => searchFieldChanged('status', e.target.value as string)}}
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
            {{tasks.data.map((task) => (
              <TableRow key={{task.id}}>
                <TableCell>{{task.id}}</TableCell>
                <TableCell>
                  <img src={{task.image_path}} style={{{{ width: 60 }}}} alt={{task.name}} />
                </TableCell>
                {{!hideProjectColumn && (
                  <TableCell>{{task.project?.name}}</TableCell>
                )}}
                <TableCell>
                  <Link href={{route('task.show', task.id)}} className="text-gray-100 hover:underline">
                    {{task.name}}
                  </Link>
                </TableCell>
                <TableCell>
                  <span className={{`px-2 py-1 rounded text-nowrap text-white ${{TASK_STATUS_CLASS_MAP[task.status]}}`}}>
                    {{TASK_STATUS_TEXT_MAP[task.status]}}
                  </span>
                </TableCell>
                <TableCell>{{task.created_at}}</TableCell>
                <TableCell>{{task.due_date}}</TableCell>
                <TableCell>{{task.createdBy.name}}</TableCell>
                <TableCell align="right">
                  <Link
                    href={{route('task.edit', task.id)}}
                    className="font-medium text-blue-600 dark:text-blue-500 hover:underline mx-1"
                  >
                    Edit
                  </Link>
                  <Button
                    onClick={{() => deleteTask(task)}}
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
      <Pagination links={{tasks.meta.links}} />
    </Box>
  );
}}
"""
    return code
