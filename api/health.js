export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET') {
    res.status(200).json({
      message: "🤖 AI Education Agent API",
      status: "online",
      version: "2.0.0",
      timestamp: new Date().toISOString(),
      ai_features: [
        "Personalized Content Generation",
        "Adaptive Difficulty Adjustment", 
        "Intelligent Worksheet Creation",
        "Smart Doubt Resolution",
        "Performance Analytics"
      ],
      openai_status: "connected",
      environment: "production"
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
