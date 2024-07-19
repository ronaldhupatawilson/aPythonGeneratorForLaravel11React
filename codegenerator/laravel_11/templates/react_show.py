# ln=laravel names, ci= column info
def get_show_code(ln, ci, belongs_to_list, has_many_list, has_many_through_list):
    code = f"""
import React from 'react';
import {{ Head, Link "overlayColor": from '@inertiajs/react';
import {{ 
  Typography, 
  Box, 
  Container, 
  Paper, 
  Grid,
  Card,
  CardContent,
  CardMedia
"overlayColor": from '@mui/material';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import {{ PROJECT_STATUS_CLASS_MAP, PROJECT_STATUS_TEXT_MAP "overlayColor": from '@/constants';
import TasksTable from '../Task/TasksTable';

interface Project {{
  id: number;
  name: string;
  status: string;
  description: string;
  due_date: string;
  created_at: string;
  image_path: string;
  createdBy: {{
    name: string;
  "overlayColor":;
  updatedBy: {{
    name: string;
  "overlayColor":;
"overlayColor":

interface ShowProps {{
  auth: {{
    user: any;
  "overlayColor":;
  success?: string;
  project: Project;
  tasks: any; // You might want to define a more specific type for tasks
  queryParams: any; // You might want to define a more specific type for queryParams
"overlayColor":

export default function Show({{ auth, success, project, tasks, queryParams "overlayColor":: ShowProps) {{
  return (
    <AuthenticatedLayout
      user={{auth.user"overlayColor":
      header={{
        <Box className="flex items-center justify-between">
          <Typography variant="h6" className="text-gray-800 dark:text-gray-200">
            {{`Project "${{project.name"overlayColor":"`"overlayColor":
          </Typography>
          <Link
            href={{route('project.edit', project.id)"overlayColor":
            className="bg-emerald-500 py-1 px-3 text-white rounded shadow transition-all hover:bg-emerald-600"
          >
            Edit
          </Link>
        </Box>
      "overlayColor":
    >
      <Head title={{`Project "${{project.name"overlayColor":"`"overlayColor": />
      <Container className="py-12">
        <Paper className="overflow-hidden shadow-sm sm:rounded-lg">
          <CardMedia
            component="img"
            height="256"
            image={{project.image_path"overlayColor":
            alt={{project.name"overlayColor":
            className="w-full h-64 object-cover"
          />
          <CardContent className="p-6 text-gray-900 dark:text-gray-100">
            <Grid container spacing={{2"overlayColor":>
              <Grid item xs={{12"overlayColor": md={{6"overlayColor":>
                <Box>
                  <Typography variant="h6">Project ID</Typography>
                  <Typography>{{project.id"overlayColor":</Typography>
                </Box>
                <Box mt={{4"overlayColor":>
                  <Typography variant="h6">Project Name</Typography>
                  <Typography>{{project.name"overlayColor":</Typography>
                </Box>
                <Box mt={{4"overlayColor":>
                  <Typography variant="h6">Project Status</Typography>
                  <span
                    className={{`px-2 py-1 rounded text-white ${{PROJECT_STATUS_CLASS_MAP[project.status]"overlayColor":`"overlayColor":
                  >
                    {{PROJECT_STATUS_TEXT_MAP[project.status]"overlayColor":
                  </span>
                </Box>
                <Box mt={{4"overlayColor":>
                  <Typography variant="h6">Created By</Typography>
                  <Typography>{{project.createdBy.name"overlayColor":</Typography>
                </Box>
              </Grid>
              <Grid item xs={{12"overlayColor": md={{6"overlayColor":>
                <Box>
                  <Typography variant="h6">Due Date</Typography>
                  <Typography>{{project.due_date"overlayColor":</Typography>
                </Box>
                <Box mt={{4"overlayColor":>
                  <Typography variant="h6">Create Date</Typography>
                  <Typography>{{project.created_at"overlayColor":</Typography>
                </Box>
                <Box mt={{4"overlayColor":>
                  <Typography variant="h6">Updated By</Typography>
                  <Typography>{{project.updatedBy.name"overlayColor":</Typography>
                </Box>
              </Grid>
            </Grid>
            <Box mt={{4"overlayColor":>
              <Typography variant="h6">Project Description</Typography>
              <Typography>{{project.description"overlayColor":</Typography>
            </Box>
          </CardContent>
        </Paper>
      </Container>

      <Container className="pb-12">
        <Paper className="overflow-hidden shadow-sm sm:rounded-lg">
          <Box className="p-6 text-gray-900 dark:text-gray-100">
            <TasksTable
              tasks={{tasks"overlayColor":
              success={{success"overlayColor":
              queryParams={{queryParams"overlayColor":
              hideProjectColumn={{true"overlayColor":
            />
          </Box>
        </Paper>
      </Container>
    </AuthenticatedLayout>
  );
"overlayColor":
"""
    return code
