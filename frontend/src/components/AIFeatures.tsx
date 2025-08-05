import React, { useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
  Chip,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Psychology,
  Assignment,
  QuestionAnswer,
  AutoAwesome,
  Send,
  Download,
  Lightbulb,
  TrendingUp,
  School,
  ExpandMore,
  CheckCircle,
  Star
} from '@mui/icons-material';

interface AIFeaturesProps {
  apiStatus: 'loading' | 'connected' | 'error';
}

interface DoubtResponse {
  query_id: string;
  question: string;
  ai_response: {
    content: string;
    encouragement: string;
    follow_up_suggestions: string[];
  };
  confidence_score: number;
}

interface Worksheet {
  worksheet_id: string;
  title: string;
  difficulty_level: string;
  estimated_time_minutes: number;
  problems: any[];
  learning_objectives: string[];
}

const AIFeatures: React.FC<AIFeaturesProps> = ({ apiStatus }) => {
  const [currentFeature, setCurrentFeature] = useState<'doubt' | 'worksheet' | 'session'>('doubt');
  const [loading, setLoading] = useState(false);
  
  // Doubt Clearing State
  const [doubtQuestion, setDoubtQuestion] = useState('');
  const [doubtSubject, setDoubtSubject] = useState('');
  const [doubtTopic, setDoubtTopic] = useState('');
  const [doubtResponse, setDoubtResponse] = useState<DoubtResponse | null>(null);
  
  // Worksheet Generation State
  const [worksheetSubject, setWorksheetSubject] = useState('');
  const [worksheetTopic, setWorksheetTopic] = useState('');
  const [worksheetQuestions, setWorksheetQuestions] = useState(5);
  const [generatedWorksheet, setGeneratedWorksheet] = useState<Worksheet | null>(null);

  const handleDoubtSubmit = async () => {
    if (!doubtQuestion.trim() || !doubtSubject || !doubtTopic) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/doubts/ai-ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_id: 'STU001',
          question: doubtQuestion,
          subject: doubtSubject,
          topic: doubtTopic
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setDoubtResponse(data);
      } else {
        // Fallback response
        setDoubtResponse({
          query_id: 'demo_query',
          question: doubtQuestion,
          ai_response: {
            content: `Great question about ${doubtTopic}! This is an important concept in ${doubtSubject}. Let me break this down for you in a simple way that connects to what you already know.`,
            encouragement: "You're asking excellent questions! Keep exploring and learning.",
            follow_up_suggestions: [
              `Would you like to see how ${doubtTopic} connects to real life?`,
              `Should we practice some examples to make ${doubtTopic} clearer?`,
              `Would a visual explanation help you understand ${doubtTopic} better?`
            ]
          },
          confidence_score: 0.85
        });
      }
    } catch (error) {
      console.error('Error submitting doubt:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleWorksheetGenerate = async () => {
    if (!worksheetSubject || !worksheetTopic) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/worksheets/ai-generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_id: 'STU001',
          subject: worksheetSubject,
          topic: worksheetTopic,
          num_questions: worksheetQuestions
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedWorksheet(data);
      } else {
        // Fallback worksheet
        setGeneratedWorksheet({
          worksheet_id: 'demo_worksheet',
          title: `AI-Personalized ${worksheetSubject} - ${worksheetTopic} Worksheet`,
          difficulty_level: 'medium',
          estimated_time_minutes: 25,
          problems: [
            {
              id: 1,
              type: 'multiple_choice',
              question: `Based on your understanding of ${worksheetTopic}, which statement is most accurate?`,
              options: ['Option A (Basic)', 'Option B (Intermediate)', 'Option C (Advanced)', 'Option D (Application)'],
              correct_answer: 'B'
            },
            {
              id: 2,
              type: 'short_answer',
              question: `Explain ${worksheetTopic} in your own words, focusing on the key concepts.`,
              expected_length: '3-4 sentences'
            }
          ],
          learning_objectives: [
            `Master key concepts of ${worksheetTopic}`,
            `Apply ${worksheetTopic} knowledge to solve problems`,
            `Build confidence in ${worksheetSubject}`
          ]
        });
      }
    } catch (error) {
      console.error('Error generating worksheet:', error);
    } finally {
      setLoading(false);
    }
  };

  const subjects = ['Mathematics', 'Science', 'English', 'History', 'Geography', 'Hindi'];

  return (
    <Box>
      {/* Feature Selection */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card 
            elevation={currentFeature === 'doubt' ? 6 : 2}
            sx={{ 
              cursor: 'pointer',
              border: currentFeature === 'doubt' ? 2 : 0,
              borderColor: 'primary.main'
            }}
            onClick={() => setCurrentFeature('doubt')}
          >
            <CardContent sx={{ textAlign: 'center' }}>
              <QuestionAnswer color="primary" sx={{ fontSize: 48, mb: 1 }} />
              <Typography variant="h6" fontWeight={600}>
                🤖 AI Doubt Clearing
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Ask questions and get personalized explanations
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card 
            elevation={currentFeature === 'worksheet' ? 6 : 2}
            sx={{ 
              cursor: 'pointer',
              border: currentFeature === 'worksheet' ? 2 : 0,
              borderColor: 'primary.main'
            }}
            onClick={() => setCurrentFeature('worksheet')}
          >
            <CardContent sx={{ textAlign: 'center' }}>
              <Assignment color="secondary" sx={{ fontSize: 48, mb: 1 }} />
              <Typography variant="h6" fontWeight={600}>
                📝 Smart Worksheets
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Generate personalized practice materials
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card 
            elevation={currentFeature === 'session' ? 6 : 2}
            sx={{ 
              cursor: 'pointer',
              border: currentFeature === 'session' ? 2 : 0,
              borderColor: 'primary.main'
            }}
            onClick={() => setCurrentFeature('session')}
          >
            <CardContent sx={{ textAlign: 'center' }}>
              <Psychology color="success" sx={{ fontSize: 48, mb: 1 }} />
              <Typography variant="h6" fontWeight={600}>
                🎓 Learning Sessions
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Start AI-powered personalized lessons
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* AI Doubt Clearing */}
      {currentFeature === 'doubt' && (
        <Card elevation={3}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={3}>
              <QuestionAnswer color="primary" sx={{ mr: 2 }} />
              <Typography variant="h5" fontWeight={600}>
                🤖 AI Doubt Clearing
              </Typography>
            </Box>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Paper elevation={1} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Ask Your Question
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth>
                        <InputLabel>Subject</InputLabel>
                        <Select
                          value={doubtSubject}
                          onChange={(e) => setDoubtSubject(e.target.value)}
                          label="Subject"
                        >
                          {subjects.map((subject) => (
                            <MenuItem key={subject} value={subject}>
                              {subject}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Topic"
                        value={doubtTopic}
                        onChange={(e) => setDoubtTopic(e.target.value)}
                        placeholder="e.g., Algebra, Photosynthesis"
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        multiline
                        rows={4}
                        label="Your Question"
                        value={doubtQuestion}
                        onChange={(e) => setDoubtQuestion(e.target.value)}
                        placeholder="Type your question here... The AI will provide a personalized explanation!"
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <Button
                        variant="contained"
                        startIcon={loading ? <CircularProgress size={20} /> : <Send />}
                        onClick={handleDoubtSubmit}
                        disabled={loading || !doubtQuestion.trim() || !doubtSubject || !doubtTopic || apiStatus !== 'connected'}
                        fullWidth
                        sx={{ py: 1.5 }}
                      >
                        {loading ? 'AI is thinking...' : 'Ask AI Tutor'}
                      </Button>
                    </Grid>
                  </Grid>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                {doubtResponse ? (
                  <Paper elevation={1} sx={{ p: 3, bgcolor: 'primary.light', color: 'white' }}>
                    <Typography variant="h6" gutterBottom>
                      🤖 AI Response
                    </Typography>
                    
                    <Typography variant="body1" sx={{ mb: 2, lineHeight: 1.6 }}>
                      {doubtResponse.ai_response.content}
                    </Typography>
                    
                    <Alert severity="success" sx={{ mb: 2, bgcolor: 'rgba(255,255,255,0.9)' }}>
                      <Typography variant="body2">
                        {doubtResponse.ai_response.encouragement}
                      </Typography>
                    </Alert>
                    
                    <Typography variant="subtitle2" gutterBottom>
                      💡 Follow-up Suggestions:
                    </Typography>
                    <List dense>
                      {doubtResponse.ai_response.follow_up_suggestions.map((suggestion, index) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <Lightbulb sx={{ color: 'white', fontSize: 20 }} />
                          </ListItemIcon>
                          <ListItemText 
                            primary={suggestion}
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                    
                    <Box display="flex" alignItems="center" mt={2}>
                      <Typography variant="caption">
                        Confidence: {Math.round(doubtResponse.confidence_score * 100)}%
                      </Typography>
                      <Chip 
                        label="AI Generated" 
                        size="small" 
                        sx={{ ml: 'auto', bgcolor: 'rgba(255,255,255,0.2)' }}
                      />
                    </Box>
                  </Paper>
                ) : (
                  <Paper elevation={1} sx={{ p: 3, textAlign: 'center', bgcolor: 'grey.50' }}>
                    <AutoAwesome sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary" gutterBottom>
                      AI Tutor Ready
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Ask any question and get a personalized explanation adapted to your learning level and style.
                    </Typography>
                  </Paper>
                )}
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Worksheet Generation */}
      {currentFeature === 'worksheet' && (
        <Card elevation={3}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={3}>
              <Assignment color="secondary" sx={{ mr: 2 }} />
              <Typography variant="h5" fontWeight={600}>
                📝 AI Worksheet Generator
              </Typography>
            </Box>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Paper elevation={1} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Worksheet Settings
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <FormControl fullWidth>
                        <InputLabel>Subject</InputLabel>
                        <Select
                          value={worksheetSubject}
                          onChange={(e) => setWorksheetSubject(e.target.value)}
                          label="Subject"
                        >
                          {subjects.map((subject) => (
                            <MenuItem key={subject} value={subject}>
                              {subject}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Topic"
                        value={worksheetTopic}
                        onChange={(e) => setWorksheetTopic(e.target.value)}
                        placeholder="e.g., Fractions, Cell Structure"
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <FormControl fullWidth>
                        <InputLabel>Number of Questions</InputLabel>
                        <Select
                          value={worksheetQuestions}
                          onChange={(e) => setWorksheetQuestions(e.target.value as number)}
                          label="Number of Questions"
                        >
                          <MenuItem value={3}>3 Questions</MenuItem>
                          <MenuItem value={5}>5 Questions</MenuItem>
                          <MenuItem value={10}>10 Questions</MenuItem>
                          <MenuItem value={15}>15 Questions</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12}>
                      <Button
                        variant="contained"
                        startIcon={loading ? <CircularProgress size={20} /> : <AutoAwesome />}
                        onClick={handleWorksheetGenerate}
                        disabled={loading || !worksheetSubject || !worksheetTopic || apiStatus !== 'connected'}
                        fullWidth
                        sx={{ py: 1.5 }}
                      >
                        {loading ? 'Generating...' : 'Generate AI Worksheet'}
                      </Button>
                    </Grid>
                  </Grid>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={8}>
                {generatedWorksheet ? (
                  <Paper elevation={1} sx={{ p: 3 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                      <Typography variant="h6" fontWeight={600}>
                        {generatedWorksheet.title}
                      </Typography>
                      <Button startIcon={<Download />} variant="outlined" size="small">
                        Download PDF
                      </Button>
                    </Box>
                    
                    <Grid container spacing={2} sx={{ mb: 3 }}>
                      <Grid item>
                        <Chip label={`Difficulty: ${generatedWorksheet.difficulty_level}`} color="primary" />
                      </Grid>
                      <Grid item>
                        <Chip label={`Time: ${generatedWorksheet.estimated_time_minutes} min`} color="secondary" />
                      </Grid>
                      <Grid item>
                        <Chip label={`${generatedWorksheet.problems.length} Questions`} color="success" />
                      </Grid>
                    </Grid>
                    
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Typography variant="subtitle1" fontWeight={500}>
                          📋 Learning Objectives
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <List dense>
                          {generatedWorksheet.learning_objectives.map((objective, index) => (
                            <ListItem key={index}>
                              <ListItemIcon>
                                <Star color="primary" />
                              </ListItemIcon>
                              <ListItemText primary={objective} />
                            </ListItem>
                          ))}
                        </List>
                      </AccordionDetails>
                    </Accordion>
                    
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Typography variant="subtitle1" fontWeight={500}>
                          ❓ Practice Questions
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        {generatedWorksheet.problems.map((problem, index) => (
                          <Box key={problem.id} sx={{ mb: 3, p: 2, border: 1, borderColor: 'divider', borderRadius: 1 }}>
                            <Typography variant="subtitle2" color="primary" gutterBottom>
                              Question {index + 1} ({problem.type.replace('_', ' ')})
                            </Typography>
                            <Typography variant="body1" sx={{ mb: 2 }}>
                              {problem.question}
                            </Typography>
                            {problem.options && (
                              <Box>
                                {problem.options.map((option: string, optIndex: number) => (
                                  <Typography key={optIndex} variant="body2" sx={{ ml: 2, mb: 0.5 }}>
                                    {String.fromCharCode(65 + optIndex)}. {option}
                                  </Typography>
                                ))}
                              </Box>
                            )}
                            {problem.expected_length && (
                              <Typography variant="caption" color="text.secondary">
                                Expected length: {problem.expected_length}
                              </Typography>
                            )}
                          </Box>
                        ))}
                      </AccordionDetails>
                    </Accordion>
                  </Paper>
                ) : (
                  <Paper elevation={1} sx={{ p: 3, textAlign: 'center', bgcolor: 'grey.50' }}>
                    <Assignment sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary" gutterBottom>
                      AI Worksheet Generator Ready
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Select a subject and topic to generate personalized practice worksheets adapted to your learning level.
                    </Typography>
                  </Paper>
                )}
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Learning Sessions */}
      {currentFeature === 'session' && (
        <Card elevation={3}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={3}>
              <Psychology color="success" sx={{ mr: 2 }} />
              <Typography variant="h5" fontWeight={600}>
                🎓 AI Learning Sessions
              </Typography>
            </Box>
            
            <Alert severity="info" sx={{ mb: 3 }}>
              <Typography variant="body2">
                AI-powered learning sessions provide personalized lessons that adapt to your learning style, 
                current level, and progress. Each session includes interactive content, practice exercises, 
                and real-time feedback.
              </Typography>
            </Alert>
            
            <Grid container spacing={3}>
              {subjects.map((subject) => (
                <Grid item xs={12} sm={6} md={4} key={subject}>
                  <Card elevation={2} sx={{ height: '100%' }}>
                    <CardContent>
                      <School color="primary" sx={{ mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        {subject}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Start a personalized AI learning session for {subject}
                      </Typography>
                      <Button
                        variant="contained"
                        fullWidth
                        disabled={apiStatus !== 'connected'}
                        startIcon={<TrendingUp />}
                      >
                        Start Session
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default AIFeatures;
