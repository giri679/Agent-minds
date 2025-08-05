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
    return {
        "worksheet_id": f"worksheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "title": f"{request_data.get('subject', 'Subject')} - {request_data.get('topic', 'Topic')} Practice",
        "difficulty_level": request_data.get("difficulty_level", 3),
        "estimated_time_minutes": 30,
        "problems": [
            {
                "id": 1,
                "type": "multiple_choice",
                "question": f"What is the main concept in {request_data.get('topic', 'this topic')}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "A"
            },
            {
                "id": 2,
                "type": "short_answer",
                "question": f"Explain {request_data.get('topic', 'the concept')} in your own words.",
                "expected_length": "2-3 sentences"
            }
        ],
        "learning_objectives": [
            f"Understand basic concepts of {request_data.get('topic', 'the topic')}",
            f"Apply {request_data.get('topic', 'the concept')} in practical scenarios"
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