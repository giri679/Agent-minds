export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { subject, topic, num_questions } = req.body || {};
    const numQuestions = num_questions || 5;

    const worksheet = {
      worksheet_id: 'ws_' + Date.now(),
      title: `${(subject || 'Mathematics').charAt(0).toUpperCase() + (subject || 'Mathematics').slice(1)} - ${topic || 'General'}`,
      difficulty_level: 'medium',
      estimated_time_minutes: numQuestions * 2,
      problems: Array.from({length: numQuestions}, (_, i) => ({
        id: i + 1,
        question: `Sample ${subject || 'mathematics'} question ${i + 1} about ${topic || 'general concepts'}`,
        type: 'multiple_choice',
        points: 5
      })),
      learning_objectives: [
        `Master key concepts of ${topic || 'the subject'}`,
        `Apply ${topic || 'subject'} knowledge to solve problems`,
        `Build confidence in ${subject || 'mathematics'}`
      ],
      environment: "production"
    };

    res.status(200).json(worksheet);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
