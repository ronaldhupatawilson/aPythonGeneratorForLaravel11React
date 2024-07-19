# ln=laravel names, ci= column info
def get_create_code(ln, ci, belongs_to_list, has_many_list, has_many_through_list):
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

interface CreateProps {{
  auth: {{
    user: any;
  }};
}}

interface FormData {{
  image: File | null;
  name: string;
  status: string;
  description: string;
  due_date: string;
}}

export default function Create({{ auth }}: CreateProps) {{
  const {{ data, setData, post, errors }} = useForm<FormData>({{
    image: null,
    name: '',
    status: '',
    description: '',
    due_date: '',
  }});

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {{
    e.preventDefault();
    post(route('project.store'));
  }};

  return (
    <AuthenticatedLayout
      user={{auth.user}}
      header={{
        <Box className="flex justify-between items-center">
          <Typography variant="h6" className="text-gray-800 dark:text-gray-200">
            Create new Project
          </Typography>
        </Box>
      }}
    >
      <Head title="Projects" />

      <Container className="py-12">
        <Paper className="p-4 sm:p-8 bg-white dark:bg-gray-800 shadow sm:rounded-lg">
          <form onSubmit={{onSubmit}}>
            <Box className="mb-4">
              <input
                type="file"
                accept="image/*"
                onChange={{(e) => setData('image', e.target.files?.[0] || null)}}
                className="hidden"
                id="project-image-input"
              />
              <label htmlFor="project-image-input">
                <Button variant="contained" component="span">
                  Upload Project Image
                </Button>
              </label>
              {{errors.image && <Typography color="error">{{errors.image}}</Typography>}}
            </Box>

            <TextField
              fullWidth
              label="Project Name"
              value={{data.name}}
              onChange={{(e) => setData('name', e.target.value)}}
              error={{!!errors.name}}
              helperText={{errors.name}}
              className="mb-4"
            />

            <TextField
              fullWidth
              multiline
              rows={{4}}
              label="Project Description"
              value={{data.description}}
              onChange={{(e) => setData('description', e.target.value)}}
              error={{!!errors.description}}
              helperText={{errors.description}}
              className="mb-4"
            />

            <TextField
              fullWidth
              type="date"
              label="Project Deadline"
              value={{data.due_date}}
              onChange={{(e) => setData('due_date', e.target.value)}}
              error={{!!errors.due_date}}
              helperText={{errors.due_date}}
              InputLabelProps={{{{ shrink: true }}}}
              className="mb-4"
            />

            <FormControl fullWidth className="mb-4">
              <InputLabel>Project Status</InputLabel>
              <Select
                value={{data.status}}
                onChange={{(e) => setData('status', e.target.value)}}
                error={{!!errors.status}}
              >
                <MenuItem value="">Select Status</MenuItem>
                <MenuItem value="pending">Pending</MenuItem>
                <MenuItem value="in_progress">In Progress</MenuItem>
                <MenuItem value="completed">Completed</MenuItem>
              </Select>
              {{errors.status && <Typography color="error">{{errors.status}}</Typography>}}
            </FormControl>

            <Box className="mt-4 text-right">
              <Link
                href={{route('project.index')}}
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
