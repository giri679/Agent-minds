"""
Simple AI Education Agent - Basic FastAPI Application
A simplified version to get started quickly
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(
    title="AI Education Agent - Simple Version",
    description="Basic version of the personalized learning system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple data models
class StudentProfile(BaseModel):
    student_id: str
    name: str
    grade: int
    school_id: str
    current_level: float = 50.0
    strengths: List[str] = []
    weaknesses: List[str] = []
    learning_style: str = "visual"

# In-memory storage (for demo purposes)
students_db = {}
sessions_db = {}

# API Routes
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "🎓 AI Education Agent API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "features": [
            "Student Profiles",
            "Learning Sessions",
            "Progress Tracking",
            "Basic Analytics"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Education Agent",
        "timestamp": datetime.utcnow().isoformat(),
        "students_count": len(students_db),
        "sessions_count": len(sessions_db)
    }

@app.post("/api/students")
async def create_student(student: StudentProfile):
    """Create a new student profile"""
    students_db[student.student_id] = student.dict()
    return {
        "message": "Student profile created successfully",
        "student_id": student.student_id,
        "status": "created"
    }

@app.get("/api/students/{student_id}")
async def get_student(student_id: str):
    """Get student profile"""
    if student_id not in students_db:
        return {"error": "Student not found"}

    student = students_db[student_id]
    return {
        "student": student,
        "recent_sessions": [s for s in sessions_db.values() if s["student_id"] == student_id]
    }

@app.post("/api/learning-sessions")
async def start_learning_session(session_data: dict):
    """Start a new learning session"""
    session_id = f"session_{len(sessions_db) + 1}"

    session = {
        "session_id": session_id,
        "student_id": session_data.get("student_id"),
        "subject": session_data.get("subject"),
        "topic": session_data.get("topic"),
        "progress": 0.0,
        "status": "in_progress",
        "started_at": datetime.utcnow().isoformat(),
        "personalized_content": {
            "difficulty_level": 3,
            "learning_style_adaptation": "visual",
            "content_blocks": [
                {
                    "type": "explanation",
                    "title": f"Introduction to {session_data.get('topic', 'Topic')}",
                    "content": "This is a personalized explanation based on your learning level..."
                },
                {
                    "type": "example",
                    "title": "Practical Example",
                    "content": "Here's a real-world example to help you understand..."
                }
            ]
        }
    }

    sessions_db[session_id] = session
    return session

@app.post("/api/worksheets/generate")
async def generate_worksheet(request_data: dict):
    """Generate a simple worksheet"""
    subject = request_data.get('subject', 'mathematics').lower()
    topic = request_data.get('topic', 'General')
    question_type = request_data.get('type', 'mixed')
    num_questions = int(request_data.get('questions', 10))

    # Subject-specific question templates
    question_templates = {
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
    }

    # Generate problems based on type
    problems = []
    templates = question_templates.get(subject, question_templates['mathematics'])

    for i in range(min(num_questions, 3)):  # Limit to 3 for demo
        if question_type == 'mcq' or question_type == 'multiple_choice':
            mcq_template = templates['mcq'][i % len(templates['mcq'])]
            problems.append({
                "id": i + 1,
                "type": "multiple_choice",
                "question": mcq_template["question"],
                "options": mcq_template["options"],
                "correct_answer": mcq_template["correct_answer"]
            })
        elif question_type == 'short':
            problems.append({
                "id": i + 1,
                "type": "short_answer",
                "question": templates['short'][i % len(templates['short'])],
                "expected_length": "2-3 sentences"
            })
        else:  # mixed
            if i % 2 == 0:  # MCQ for even indices
                mcq_template = templates['mcq'][i % len(templates['mcq'])]
                problems.append({
                    "id": i + 1,
                    "type": "multiple_choice",
                    "question": mcq_template["question"],
                    "options": mcq_template["options"],
                    "correct_answer": mcq_template["correct_answer"]
                })
            else:  # Short answer for odd indices
                problems.append({
                    "id": i + 1,
                    "type": "short_answer",
                    "question": templates['short'][i % len(templates['short'])],
                    "expected_length": "2-3 sentences"
                })

    return {
        "worksheet_id": f"worksheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "title": f"{subject.title()} - {topic} Practice",
        "difficulty_level": request_data.get("difficulty_level", 3),
        "estimated_time_minutes": num_questions * 3,
        "problems": problems,
        "learning_objectives": [
            f"Understand basic concepts of {topic}",
            f"Apply {topic} knowledge in practical scenarios",
            f"Build confidence in {subject}"
        ]
    }

@app.post("/api/doubts/ask")
async def ask_doubt(doubt_data: dict):
    """Simple doubt clearing"""
    question = doubt_data.get("question", "")

    return {
        "query_id": f"doubt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "question": question,
        "ai_response": {
            "type": "explanation",
            "content": f"Great question! Let me help you understand this concept. {question} is an important topic that requires step-by-step understanding...",
            "examples": [
                "Example 1: Think of it like...",
                "Example 2: Another way to look at it is..."
            ],
            "follow_up_questions": [
                "Would you like me to explain this with a different approach?",
                "Do you want to see more examples?"
            ]
        },
        "confidence_score": 0.85,
        "related_topics": ["Related Topic 1", "Related Topic 2"]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Education Agent...")
    print("📚 Access the API at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)