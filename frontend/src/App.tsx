import React, { useState, useEffect } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Card,
  CardContent,
  Box,
  Button,
  Tab,
  Tabs,
  Avatar,
  Chip,
  LinearProgress,
  Alert,
  Fab
} from '@mui/material';
import {
  School,
  Psychology,
  Assignment,
  Analytics,
  QuestionAnswer,
  Person,
  Dashboard,
  AutoAwesome,
  TrendingUp,
  EmojiEvents
} from '@mui/icons-material';
import StudentDashboard from './components/StudentDashboard';
import TeacherDashboard from './components/TeacherDashboard';
import AIFeatures from './components/AIFeatures';
import './App.css';

// Create a beautiful theme for the AI Education Agent
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#9c27b0',
      light: '#ba68c8',
      dark: '#7b1fa2',
    },
    success: {
      main: '#2e7d32',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 12,
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [currentTab, setCurrentTab] = useState(0);
  const [apiStatus, setApiStatus] = useState<'loading' | 'connected' | 'error'>('loading');
  const [systemInfo, setSystemInfo] = useState<any>(null);

  useEffect(() => {
    // Check API connection on startup
    checkApiConnection();
  }, []);

  const checkApiConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/');
      const data = await response.json();
      setSystemInfo(data);
      setApiStatus('connected');
    } catch (error) {
      console.error('API connection failed:', error);
      setApiStatus('error');
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', backgroundColor: 'background.default' }}>
        {/* Header */}
        <AppBar position="static" elevation={0} sx={{ background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)' }}>
          <Toolbar>
            <AutoAwesome sx={{ mr: 2, fontSize: 32 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
              🤖 AI Education Agent - Government Schools
            </Typography>
            <Chip
              icon={apiStatus === 'connected' ? <TrendingUp /> : undefined}
              label={apiStatus === 'connected' ? 'AI Connected' : apiStatus === 'loading' ? 'Connecting...' : 'Offline'}
              color={apiStatus === 'connected' ? 'success' : apiStatus === 'loading' ? 'warning' : 'error'}
              variant="filled"
              sx={{ color: 'white', fontWeight: 500 }}
            />
          </Toolbar>
        </AppBar>

        {/* API Status Alert */}
        {apiStatus === 'error' && (
          <Alert severity="warning" sx={{ m: 2 }}>
            Backend API is not running. Please start the backend server at http://localhost:8000
            <Button onClick={checkApiConnection} sx={{ ml: 2 }}>Retry</Button>
          </Alert>
        )}

        {/* System Info Banner */}
        {systemInfo && (
          <Box sx={{ bgcolor: 'primary.light', color: 'white', p: 2, textAlign: 'center' }}>
            <Typography variant="body1">
              🎓 {systemInfo.message} | Version {systemInfo.version} |
              OpenAI Status: {systemInfo.openai_status === 'connected' ? '✅ Connected' : '❌ Not Connected'}
            </Typography>
          </Box>
        )}

        {/* Navigation Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'white' }}>
          <Tabs value={currentTab} onChange={handleTabChange} centered>
            <Tab
              icon={<Dashboard />}
              label="Student Dashboard"
              sx={{ minHeight: 72, fontWeight: 500 }}
            />
            <Tab
              icon={<Person />}
              label="Teacher Dashboard"
              sx={{ minHeight: 72, fontWeight: 500 }}
            />
            <Tab
              icon={<Psychology />}
              label="AI Features"
              sx={{ minHeight: 72, fontWeight: 500 }}
            />
          </Tabs>
        </Box>

        {/* Tab Content */}
        <Container maxWidth="xl" sx={{ mt: 3, mb: 3 }}>
          <TabPanel value={currentTab} index={0}>
            <StudentDashboard apiStatus={apiStatus} />
          </TabPanel>
          <TabPanel value={currentTab} index={1}>
            <TeacherDashboard apiStatus={apiStatus} />
          </TabPanel>
          <TabPanel value={currentTab} index={2}>
            <AIFeatures apiStatus={apiStatus} />
          </TabPanel>
        </Container>

        {/* Floating Action Button */}
        <Fab
          color="secondary"
          aria-label="AI Help"
          sx={{
            position: 'fixed',
            bottom: 16,
            right: 16,
            background: 'linear-gradient(45deg, #9c27b0 30%, #ba68c8 90%)',
          }}
          onClick={() => setCurrentTab(2)}
        >
          <AutoAwesome />
        </Fab>
      </Box>
    </ThemeProvider>
  );
}

export default App;