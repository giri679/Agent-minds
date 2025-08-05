import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Avatar,
  LinearProgress,
  Chip,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
  CircularProgress,
  IconButton
} from '@mui/material';
import {
  Person,
  TrendingUp,
  School,
  Assignment,
  Psychology,
  EmojiEvents,
  Star,
  CheckCircle,
  PlayArrow,
  Refresh
} from '@mui/icons-material';

interface StudentDashboardProps {
  apiStatus: 'loading' | 'connected' | 'error';
}

interface StudentData {
  student_id: string;
  name: string;
  grade: number;
  current_level: number;
  strengths: string[];
  weaknesses: string[];
  learning_style: string;
  academic_history: any[];
}

interface AIInsights {
  ai_analysis: any;
  learning_insights: any;
  personalized_recommendations: string[];
  study_plan: any;
  motivation_message: string;
  next_learning_session_suggestion: any;
}

const StudentDashboard: React.FC<StudentDashboardProps> = ({ apiStatus }) => {
  const [studentData, setStudentData] = useState<StudentData | null>(null);
  const [aiInsights, setAIInsights] = useState<AIInsights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Sample student ID - in real app, this would come from authentication
  const studentId = 'STU001';

  useEffect(() => {
    if (apiStatus === 'connected') {
      fetchStudentData();
      fetchAIInsights();
    }
  }, [apiStatus]);

  const fetchStudentData = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/students/${studentId}`);
      if (response.ok) {
        const data = await response.json();
        setStudentData(data.student);
      } else {
        // Use sample data if API call fails
        setStudentData({
          student_id: 'STU001',
          name: 'Priya Sharma',
          grade: 8,
          current_level: 76.0,
          strengths: ['Mathematics', 'Science'],
          weaknesses: ['English Grammar', 'History'],
          learning_style: 'visual',
          academic_history: []
        });
      }
    } catch (err) {
      console.error('Error fetching student data:', err);
      setError('Failed to load student data');
    }
  };

  const fetchAIInsights = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/api/analytics/ai-insights/${studentId}`);
      if (response.ok) {
        const data = await response.json();
        setAIInsights(data);
      }
    } catch (err) {
      console.error('Error fetching AI insights:', err);
      setError('Failed to load AI insights');
    } finally {
      setLoading(false);
    }
  };

  const getProgressColor = (level: number) => {
    if (level >= 80) return 'success';
    if (level >= 60) return 'warning';
    return 'error';
  };

  if (loading && apiStatus === 'connected') {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ ml: 2 }}>Loading your personalized dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Grid container spacing={3}>
      {/* Student Profile Card */}
      <Grid item xs={12} md={4}>
        <Card elevation={3} sx={{ height: '100%', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <CardContent sx={{ color: 'white', textAlign: 'center' }}>
            <Avatar
              sx={{
                width: 80,
                height: 80,
                margin: '0 auto 16px',
                bgcolor: 'rgba(255,255,255,0.2)',
                fontSize: '2rem'
              }}
            >
              {studentData?.name?.charAt(0) || 'P'}
            </Avatar>
            <Typography variant="h5" gutterBottom fontWeight={600}>
              {studentData?.name || 'Priya Sharma'}
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9 }}>
              Grade {studentData?.grade || 8} Student
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8, mt: 1 }}>
              Learning Style: {studentData?.learning_style || 'Visual'}
            </Typography>

            <Box sx={{ mt: 3 }}>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>Overall Progress</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={studentData?.current_level || 76}
                  sx={{
                    flexGrow: 1,
                    height: 8,
                    borderRadius: 4,
                    bgcolor: 'rgba(255,255,255,0.2)',
                    '& .MuiLinearProgress-bar': {
                      bgcolor: 'white'
                    }
                  }}
                />
                <Typography variant="body2" sx={{ ml: 1, fontWeight: 600 }}>
                  {studentData?.current_level || 76}%
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Grid>

      {/* AI Insights Card */}
      <Grid item xs={12} md={8}>
        <Card elevation={3} sx={{ height: '100%' }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <Psychology color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6" fontWeight={600}>
                🤖 AI-Powered Insights
              </Typography>
              <IconButton onClick={fetchAIInsights} size="small" sx={{ ml: 'auto' }}>
                <Refresh />
              </IconButton>
            </Box>

            {aiInsights?.motivation_message && (
              <Alert severity="success" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  {aiInsights.motivation_message}
                </Typography>
              </Alert>
            )}

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="primary" gutterBottom>
                  🎯 Strengths
                </Typography>
                <Box>
                  {(studentData?.strengths || ['Mathematics', 'Science']).map((strength, index) => (
                    <Chip
                      key={index}
                      label={strength}
                      color="success"
                      size="small"
                      sx={{ mr: 1, mb: 1 }}
                      icon={<Star />}
                    />
                  ))}
                </Box>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="warning.main" gutterBottom>
                  📚 Focus Areas
                </Typography>
                <Box>
                  {(aiInsights?.ai_analysis?.focus_areas || ['Advanced concepts']).map((area, index) => (
                    <Chip
                      key={index}
                      label={area}
                      color="warning"
                      size="small"
                      sx={{ mr: 1, mb: 1 }}
                      icon={<Assignment />}
                    />
                  ))}
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>

      {/* Subject Performance */}
      <Grid item xs={12} md={6}>
        <Card elevation={3}>
          <CardContent>
            <Typography variant="h6" gutterBottom fontWeight={600}>
              📊 Subject Performance
            </Typography>
            {aiInsights?.ai_analysis?.subject_performance ? (
              <Box>
                {Object.entries(aiInsights.ai_analysis.subject_performance).map(([subject, score], index) => (
                  <Box key={subject} sx={{ mb: 2 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Typography variant="body2">{subject}</Typography>
                      <Typography variant="body2" fontWeight={600}>
                        {Math.round(score as number)}%
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={score as number}
                      color={getProgressColor(score as number)}
                      sx={{ height: 6, borderRadius: 3, mt: 0.5 }}
                    />
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Performance data will appear here once you complete some assessments.
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>

      {/* Study Plan */}
      <Grid item xs={12} md={6}>
        <Card elevation={3}>
          <CardContent>
            <Typography variant="h6" gutterBottom fontWeight={600}>
              📅 Personalized Study Plan
            </Typography>
            {aiInsights?.study_plan ? (
              <Box>
                <Typography variant="subtitle2" color="primary" gutterBottom>
                  Daily Goals
                </Typography>
                <List dense>
                  {aiInsights.study_plan.daily_goals?.map((goal: string, index: number) => (
                    <ListItem key={index} sx={{ py: 0.5 }}>
                      <ListItemIcon sx={{ minWidth: 32 }}>
                        <CheckCircle color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={goal} />
                    </ListItem>
                  ))}
                </List>

                <Divider sx={{ my: 2 }} />

                <Typography variant="subtitle2" color="secondary" gutterBottom>
                  Weekly Goals
                </Typography>
                <List dense>
                  {aiInsights.study_plan.weekly_goals?.map((goal: string, index: number) => (
                    <ListItem key={index} sx={{ py: 0.5 }}>
                      <ListItemIcon sx={{ minWidth: 32 }}>
                        <EmojiEvents color="warning" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={goal} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Your personalized study plan will be generated based on your performance.
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>

      {/* Quick Actions */}
      <Grid item xs={12}>
        <Card elevation={3}>
          <CardContent>
            <Typography variant="h6" gutterBottom fontWeight={600}>
              🚀 Quick Actions
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<PlayArrow />}
                  sx={{ py: 1.5 }}
                  disabled={apiStatus !== 'connected'}
                >
                  Start Learning Session
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Assignment />}
                  sx={{ py: 1.5 }}
                  disabled={apiStatus !== 'connected'}
                >
                  Generate Worksheet
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Psychology />}
                  sx={{ py: 1.5 }}
                  disabled={apiStatus !== 'connected'}
                >
                  Ask AI Tutor
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<TrendingUp />}
                  sx={{ py: 1.5 }}
                  disabled={apiStatus !== 'connected'}
                >
                  View Progress
                </Button>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default StudentDashboard;