import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Button,
  Avatar,
  LinearProgress,
  Alert,
  CircularProgress,
  IconButton,
  Tabs,
  Tab
} from '@mui/material';
import {
  People,
  TrendingUp,
  Assignment,
  Psychology,
  School,
  Analytics,
  Refresh,
  Add,
  Download,
  Visibility
} from '@mui/icons-material';

interface TeacherDashboardProps {
  apiStatus: 'loading' | 'connected' | 'error';
}

interface Student {
  student_id: string;
  name: string;
  grade: number;
  current_level: number;
  strengths: string[];
  weaknesses: string[];
  last_activity: string;
  status: 'active' | 'inactive';
}

interface ClassStats {
  total_students: number;
  average_performance: number;
  active_sessions: number;
  completed_worksheets: number;
  pending_doubts: number;
}

const TeacherDashboard: React.FC<TeacherDashboardProps> = ({ apiStatus }) => {
  const [students, setStudents] = useState<Student[]>([]);
  const [classStats, setClassStats] = useState<ClassStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentTab, setCurrentTab] = useState(0);

  useEffect(() => {
    if (apiStatus === 'connected') {
      fetchClassData();
    } else {
      // Use sample data when API is not connected
      setStudents([
        {
          student_id: 'STU001',
          name: 'Priya Sharma',
          grade: 8,
          current_level: 76.0,
          strengths: ['Mathematics', 'Science'],
          weaknesses: ['English Grammar'],
          last_activity: '2024-01-15T10:30:00Z',
          status: 'active'
        },
        {
          student_id: 'STU002',
          name: 'Rahul Kumar',
          grade: 8,
          current_level: 68.5,
          strengths: ['History', 'Geography'],
          weaknesses: ['Mathematics', 'Science'],
          last_activity: '2024-01-15T09:15:00Z',
          status: 'active'
        },
        {
          student_id: 'STU003',
          name: 'Anita Singh',
          grade: 8,
          current_level: 82.0,
          strengths: ['English', 'Science'],
          weaknesses: ['Mathematics'],
          last_activity: '2024-01-14T16:45:00Z',
          status: 'inactive'
        }
      ]);
      
      setClassStats({
        total_students: 25,
        average_performance: 72.5,
        active_sessions: 8,
        completed_worksheets: 45,
        pending_doubts: 12
      });
      
      setLoading(false);
    }
  }, [apiStatus]);

  const fetchClassData = async () => {
    try {
      setLoading(true);
      // In a real app, this would fetch actual class data
      // For now, we'll use the sample data above
      setLoading(false);
    } catch (error) {
      console.error('Error fetching class data:', error);
      setLoading(false);
    }
  };

  const getPerformanceColor = (level: number) => {
    if (level >= 80) return 'success';
    if (level >= 60) return 'warning';
    return 'error';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-IN');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ ml: 2 }}>Loading class dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Class Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <People color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight={600} color="primary">
                {classStats?.total_students || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Students
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <TrendingUp color="success" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight={600} color="success.main">
                {classStats?.average_performance || 0}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Avg Performance
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <School color="info" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight={600} color="info.main">
                {classStats?.active_sessions || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Active Sessions
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <Assignment color="secondary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight={600} color="secondary.main">
                {classStats?.completed_worksheets || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Worksheets Done
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <Psychology color="warning" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight={600} color="warning.main">
                {classStats?.pending_doubts || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Pending Doubts
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content */}
      <Card elevation={3}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={currentTab} onChange={(e, newValue) => setCurrentTab(newValue)}>
            <Tab label="Student Overview" />
            <Tab label="Performance Analytics" />
            <Tab label="AI Insights" />
          </Tabs>
        </Box>

        <CardContent>
          {currentTab === 0 && (
            <Box>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                <Typography variant="h6" fontWeight={600}>
                  👥 Class 8 - Student Overview
                </Typography>
                <Box>
                  <Button
                    startIcon={<Add />}
                    variant="contained"
                    sx={{ mr: 1 }}
                    disabled={apiStatus !== 'connected'}
                  >
                    Add Student
                  </Button>
                  <Button
                    startIcon={<Download />}
                    variant="outlined"
                    sx={{ mr: 1 }}
                  >
                    Export
                  </Button>
                  <IconButton onClick={fetchClassData}>
                    <Refresh />
                  </IconButton>
                </Box>
              </Box>

              <TableContainer component={Paper} elevation={0} sx={{ border: 1, borderColor: 'divider' }}>
                <Table>
                  <TableHead>
                    <TableRow sx={{ bgcolor: 'grey.50' }}>
                      <TableCell>Student</TableCell>
                      <TableCell>Performance</TableCell>
                      <TableCell>Strengths</TableCell>
                      <TableCell>Focus Areas</TableCell>
                      <TableCell>Last Activity</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {students.map((student) => (
                      <TableRow key={student.student_id} hover>
                        <TableCell>
                          <Box display="flex" alignItems="center">
                            <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                              {student.name.charAt(0)}
                            </Avatar>
                            <Box>
                              <Typography variant="body2" fontWeight={500}>
                                {student.name}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                ID: {student.student_id}
                              </Typography>
                            </Box>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box sx={{ minWidth: 120 }}>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                              <Typography variant="body2" fontWeight={500}>
                                {student.current_level}%
                              </Typography>
                            </Box>
                            <LinearProgress
                              variant="determinate"
                              value={student.current_level}
                              color={getPerformanceColor(student.current_level)}
                              sx={{ mt: 0.5, height: 6, borderRadius: 3 }}
                            />
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box>
                            {student.strengths.slice(0, 2).map((strength, index) => (
                              <Chip
                                key={index}
                                label={strength}
                                size="small"
                                color="success"
                                sx={{ mr: 0.5, mb: 0.5 }}
                              />
                            ))}
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box>
                            {student.weaknesses.slice(0, 2).map((weakness, index) => (
                              <Chip
                                key={index}
                                label={weakness}
                                size="small"
                                color="warning"
                                sx={{ mr: 0.5, mb: 0.5 }}
                              />
                            ))}
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {formatDate(student.last_activity)}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={student.status}
                            color={student.status === 'active' ? 'success' : 'default'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          <IconButton size="small" color="primary">
                            <Visibility />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}

          {currentTab === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                📊 Performance Analytics
              </Typography>
              <Alert severity="info">
                Detailed performance analytics and charts will be displayed here.
                This includes subject-wise performance, learning trends, and comparative analysis.
              </Alert>
            </Box>
          )}

          {currentTab === 2 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                🤖 AI-Powered Class Insights
              </Typography>
              <Alert severity="success" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  <strong>AI Recommendation:</strong> Focus on Mathematics support for 40% of students. 
                  Consider group study sessions for English Grammar improvement.
                </Typography>
              </Alert>
              <Typography variant="body2" color="text.secondary">
                AI insights include personalized recommendations for each student, 
                class-wide learning patterns, and suggested interventions.
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default TeacherDashboard;
