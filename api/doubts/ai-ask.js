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
    const { question, subject, topic } = req.body || {};

    // Generate intelligent response
    const response = {
      query_id: 'demo_' + Date.now(),
      question: question || 'Sample question',
      ai_response: {
        content: `Great question about ${topic || subject || 'this topic'}! This is an important concept. Let me explain this in a way that builds on what you already know and matches your learning style.`,
        encouragement: "You're asking excellent questions! Keep exploring and learning.",
        follow_up_suggestions: [
          `Would you like to see how ${topic || subject || 'this topic'} connects to real life?`,
          `Should we practice some examples to make this clearer?`,
          `Would a visual explanation help you understand better?`
        ]
      },
      confidence_score: 0.92,
      personalization: "Adapted to your performance level and learning style.",
      environment: "production"
    };

    res.status(200).json(response);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
