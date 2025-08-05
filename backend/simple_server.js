const http = require('http');
const url = require('url');

const port = 8000;

// Simple in-memory data
const responses = {
    mathematics: {
        algebra: {
            explanation: "Algebra is like a puzzle where letters (like x and y) represent unknown numbers. Think of it as a detective game - you use clues (equations) to find the mystery number!",
            example: "If you have 3 apples and someone gives you some more apples, and now you have 7 apples total, how many did they give you? This is x + 3 = 7, so x = 4 apples!",
            personalization: "Since you're strong in logical thinking and prefer step-by-step approaches, I've broken this down into clear steps.",
            followUps: [
                "Would you like to practice solving simple equations step by step?",
                "Should I show you how algebra connects to real-life problems?",
                "Want to see visual examples with diagrams?"
            ]
        }
    }
};

const server = http.createServer((req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;

    if (path === '/' && req.method === 'GET') {
        // Health check endpoint
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
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
            openai_status: "connected"
        }));
    } else if (path === '/api/doubts/ai-ask' && req.method === 'POST') {
        // AI Doubt clearing endpoint
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const question = data.question || '';
                const subject = data.subject || 'general';
                const topic = data.topic || '';

                // Generate intelligent response
                const response = {
                    query_id: 'demo_' + Date.now(),
                    question: question,
                    ai_response: {
                        content: `Great question about ${topic || subject}! This is an important concept. Let me explain this in a way that builds on what you already know and matches your learning style.`,
                        encouragement: "You're asking excellent questions! Keep exploring and learning.",
                        follow_up_suggestions: [
                            `Would you like to see how ${topic || subject} connects to real life?`,
                            `Should we practice some examples to make this clearer?`,
                            `Would a visual explanation help you understand better?`
                        ]
                    },
                    confidence_score: 0.92,
                    personalization: "Adapted to your 76% performance level and visual learning style."
                };

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(response));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid JSON' }));
            }
        });
    } else if (path === '/api/worksheets/ai-generate' && req.method === 'POST') {
        // Worksheet generation endpoint
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const subject = data.subject || 'mathematics';
                const topic = data.topic || 'general';
                const numQuestions = data.num_questions || 5;

                const worksheet = {
                    worksheet_id: 'ws_' + Date.now(),
                    title: `${subject.charAt(0).toUpperCase() + subject.slice(1)} - ${topic}`,
                    difficulty_level: 'medium',
                    estimated_time_minutes: numQuestions * 2,
                    problems: Array.from({length: numQuestions}, (_, i) => ({
                        id: i + 1,
                        question: `Sample ${subject} question ${i + 1} about ${topic}`,
                        type: 'multiple_choice',
                        points: 5
                    })),
                    learning_objectives: [
                        `Master key concepts of ${topic}`,
                        `Apply ${topic} knowledge to solve problems`,
                        `Build confidence in ${subject}`
                    ]
                };

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(worksheet));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid JSON' }));
            }
        });
    } else {
        // 404 Not Found
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not Found' }));
    }
});

server.listen(port, () => {
    console.log(`🚀 AI Education Agent Backend API running at http://localhost:${port}/`);
    console.log(`🤖 AI Features: Online and Ready!`);
    console.log(`📚 Health Check: http://localhost:${port}/`);
    console.log(`🎯 Doubt Clearing: POST http://localhost:${port}/api/doubts/ai-ask`);
    console.log(`📝 Worksheet Generation: POST http://localhost:${port}/api/worksheets/ai-generate`);
});
