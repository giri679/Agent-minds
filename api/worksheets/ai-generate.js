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
    const { subject, topic, questions, type, difficulty_level } = req.body || {};
    const numQuestions = parseInt(questions) || 5;
    const questionType = type || 'mixed';
    const subjectLower = (subject || 'mathematics').toLowerCase();

    // Subject-specific question templates
    const questionTemplates = {
      'mathematics': {
        'mcq': [
          {
            "question": "What is the value of x in the equation 2x + 5 = 13?",
            "options": ["A) x = 3", "B) x = 4", "C) x = 5", "D) x = 6"],
            "correct_answer": "B"
          },
          {
            "question": "If y = 3x - 2, what is the value of y when x = 4?",
            "options": ["A) y = 8", "B) y = 10", "C) y = 12", "D) y = 14"],
            "correct_answer": "B"
          },
          {
            "question": "What is the simplified form of 4(x + 3) - 2x?",
            "options": ["A) 2x + 12", "B) 4x + 12", "C) 2x + 3", "D) 6x + 12"],
            "correct_answer": "A"
          }
        ],
        'short': [
          "Solve for x: 2x + 5 = 13. Show your work step by step.",
          "If y = 3x - 2, find y when x = 4. Explain your calculation.",
          "Simplify: 4(x + 3) - 2x. Show each step of the simplification."
        ]
      },
      'science': {
        'mcq': [
          {
            "question": "What is the primary function of mitochondria in a cell?",
            "options": ["A) Protein synthesis", "B) Energy production", "C) DNA storage", "D) Waste removal"],
            "correct_answer": "B"
          },
          {
            "question": "Which process do plants use to make their own food?",
            "options": ["A) Respiration", "B) Digestion", "C) Photosynthesis", "D) Transpiration"],
            "correct_answer": "C"
          },
          {
            "question": "What are the three main states of matter?",
            "options": ["A) Hot, cold, warm", "B) Solid, liquid, gas", "C) Big, medium, small", "D) Fast, slow, still"],
            "correct_answer": "B"
          }
        ],
        'short': [
          "Explain the function of mitochondria in a cell and why they are called 'powerhouses'.",
          "Describe the process of photosynthesis and explain why it's important for life on Earth.",
          "List the three states of matter and give two examples of each state."
        ]
      },
      'history': {
        'mcq': [
          {
            "question": "Who was the first Prime Minister of India?",
            "options": ["A) Mahatma Gandhi", "B) Jawaharlal Nehru", "C) Sardar Patel", "D) Dr. Rajendra Prasad"],
            "correct_answer": "B"
          },
          {
            "question": "In which year did India gain independence?",
            "options": ["A) 1945", "B) 1946", "C) 1947", "D) 1948"],
            "correct_answer": "C"
          },
          {
            "question": "Which movement was led by Mahatma Gandhi for Indian independence?",
            "options": ["A) Quit India Movement", "B) Khilafat Movement", "C) Swadeshi Movement", "D) All of the above"],
            "correct_answer": "D"
          }
        ],
        'short': [
          "Name the first Prime Minister of India and describe one of his major contributions.",
          "Explain the significance of August 15, 1947, in Indian history.",
          "List three important leaders of the Indian freedom struggle and their contributions."
        ]
      }
    };

    // Generate problems based on type
    const problems = [];
    const templates = questionTemplates[subjectLower] || questionTemplates['mathematics'];

    for (let i = 0; i < Math.min(numQuestions, 3); i++) {
      if (questionType === 'mcq' || questionType === 'multiple_choice') {
        const mcqTemplate = templates['mcq'][i % templates['mcq'].length];
        problems.push({
          "id": i + 1,
          "type": "multiple_choice",
          "question": mcqTemplate.question,
          "options": mcqTemplate.options,
          "correct_answer": mcqTemplate.correct_answer
        });
      } else if (questionType === 'short') {
        problems.push({
          "id": i + 1,
          "type": "short_answer",
          "question": templates['short'][i % templates['short'].length],
          "expected_length": "2-3 sentences"
        });
      } else { // mixed
        if (i % 2 === 0) {
          const mcqTemplate = templates['mcq'][i % templates['mcq'].length];
          problems.push({
            "id": i + 1,
            "type": "multiple_choice",
            "question": mcqTemplate.question,
            "options": mcqTemplate.options,
            "correct_answer": mcqTemplate.correct_answer
          });
        } else {
          problems.push({
            "id": i + 1,
            "type": "short_answer",
            "question": templates['short'][i % templates['short'].length],
            "expected_length": "2-3 sentences"
          });
        }
      }
    }

    const worksheet = {
      worksheet_id: 'ws_' + Date.now(),
      title: `${subject?.charAt(0).toUpperCase() + subject?.slice(1) || 'Mathematics'} - ${topic || 'General'}`,
      difficulty_level: difficulty_level || 'medium',
      estimated_time_minutes: numQuestions * 3,
      problems: problems,
      learning_objectives: [
        `Understand basic concepts of ${topic || 'the topic'}`,
        `Apply ${topic || 'subject'} knowledge in practical scenarios`,
        `Build confidence in ${subject || 'mathematics'}`
      ],
      environment: "production"
    };

    res.status(200).json(worksheet);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
