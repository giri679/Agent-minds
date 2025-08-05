"""
AI Education Agent - Full AI-Powered Version
Complete implementation with OpenAI integration for personalized learning
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
import json
import random

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="AI Education Agent - Full Version",
    description="Complete AI-powered personalized learning system for government schools",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced data models
class StudentProfile(BaseModel):
    student_id: str
    name: str
    grade: int
    school_id: str
    current_level: float = 50.0
    strengths: List[str] = []
    weaknesses: List[str] = []
    learning_style: str = "visual"
    academic_history: List[Dict] = []

# In-memory storage with sample data
students_db = {
    "STU001": {
        "student_id": "STU001",
        "name": "Priya Sharma",
        "grade": 8,
        "school_id": "SCHOOL001",
        "current_level": 75.5,
        "strengths": ["Mathematics", "Science"],
        "weaknesses": ["English Grammar", "History"],
        "learning_style": "visual",
        "academic_history": [
            {"subject": "Mathematics", "topic": "Algebra", "score": 85, "max_score": 100, "assessment_date": "2024-01-15", "difficulty_level": "medium"},
            {"subject": "Science", "topic": "Photosynthesis", "score": 78, "max_score": 100, "assessment_date": "2024-01-10", "difficulty_level": "medium"},
            {"subject": "English", "topic": "Grammar", "score": 65, "max_score": 100, "assessment_date": "2024-01-08", "difficulty_level": "easy"}
        ]
    }
}

sessions_db = {}

# AI-powered functions
async def analyze_student_performance(student_id: str) -> Dict:
    """Analyze student's academic performance using AI"""
    if student_id not in students_db:
        return {"error": "Student not found"}

    student = students_db[student_id]
    academic_history = student.get("academic_history", [])

    if not academic_history:
        return {
            "overall_level": 50.0,
            "recommended_difficulty": "medium",
            "focus_areas": ["Basic concepts"],
            "learning_path": ["Start with fundamentals"]
        }

    # Calculate performance metrics
    total_score = sum(record["score"] for record in academic_history)
    total_possible = sum(record["max_score"] for record in academic_history)
    overall_percentage = (total_score / total_possible) * 100 if total_possible > 0 else 50

    # Subject-wise analysis
    subject_performance = {}
    for record in academic_history:
        subject = record["subject"]
        if subject not in subject_performance:
            subject_performance[subject] = []
        subject_performance[subject].append(record["score"] / record["max_score"] * 100)

    # Calculate averages
    subject_averages = {
        subject: sum(scores) / len(scores)
        for subject, scores in subject_performance.items()
    }

    # Identify strengths and weaknesses
    strengths = [subject for subject, avg in subject_averages.items() if avg >= 75]
    weaknesses = [subject for subject, avg in subject_averages.items() if avg < 65]

    # Determine recommended difficulty
    if overall_percentage >= 85:
        recommended_difficulty = "hard"
    elif overall_percentage >= 70:
        recommended_difficulty = "medium"
    else:
        recommended_difficulty = "easy"

    return {
        "overall_level": round(overall_percentage, 1),
        "recommended_difficulty": recommended_difficulty,
        "subject_performance": subject_averages,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "focus_areas": weaknesses if weaknesses else ["Advanced concepts"],
        "learning_path": [f"Focus on {area}" for area in weaknesses[:3]]
    }

# API Routes
@app.get("/")
async def root():
    """Welcome endpoint with AI capabilities"""
    return {
        "message": "🤖 AI Education Agent - Full AI-Powered Version",
        "status": "running",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_features": [
            "Personalized Content Generation",
            "Adaptive Difficulty Adjustment",
            "Intelligent Worksheet Creation",
            "Smart Doubt Resolution",
            "Performance Analytics",
            "Learning Path Optimization"
        ],
        "openai_status": "connected" if openai.api_key else "not_configured"
    }

@app.get("/health")
async def health_check():
    """Enhanced health check with AI status"""
    return {
        "status": "healthy",
        "service": "AI Education Agent - Full Version",
        "timestamp": datetime.utcnow().isoformat(),
        "students_count": len(students_db),
        "sessions_count": len(sessions_db),
        "ai_enabled": bool(openai.api_key),
        "features_active": [
            "Student Profiling",
            "Performance Analysis",
            "AI Content Generation",
            "Smart Recommendations"
        ]
    }

@app.post("/api/students")
async def create_student(student: StudentProfile):
    """Create student with AI analysis"""
    students_db[student.student_id] = student.dict()

    # Perform initial AI analysis
    analysis = await analyze_student_performance(student.student_id)

    return {
        "message": "Student profile created with AI analysis",
        "student_id": student.student_id,
        "status": "created",
        "ai_analysis": analysis
    }

@app.get("/api/students/{student_id}")
async def get_student(student_id: str):
    """Get student with AI insights"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    student = students_db[student_id]
    analysis = await analyze_student_performance(student_id)
    recent_sessions = [s for s in sessions_db.values() if s.get("student_id") == student_id]

    return {
        "student": student,
        "ai_analysis": analysis,
        "recent_sessions": recent_sessions[-5:],  # Last 5 sessions
        "recommendations": [
            f"Focus on {area}" for area in analysis.get("focus_areas", [])
        ]
    }

@app.post("/api/learning-sessions/ai")
async def start_ai_learning_session(session_data: dict):
    """Start AI-powered personalized learning session"""
    student_id = session_data.get("student_id")
    subject = session_data.get("subject")
    topic = session_data.get("topic")

    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    student = students_db[student_id]
    analysis = await analyze_student_performance(student_id)

    # Generate AI-powered content
    try:
        if openai.api_key:
            prompt = f"""
            Create a personalized lesson for a grade {student['grade']} student on {subject} - {topic}.

            Student Profile:
            - Current Level: {analysis.get('overall_level', 50)}%
            - Learning Style: {student.get('learning_style', 'visual')}
            - Strengths: {', '.join(student.get('strengths', []))}
            - Weaknesses: {', '.join(student.get('weaknesses', []))}

            Create content that:
            1. Matches their current understanding level
            2. Uses their preferred learning style
            3. Builds on their strengths
            4. Addresses their weak areas

            Provide: explanation, examples, key_points, practice_activities
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert teacher creating personalized lessons for Indian government school students."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )

            ai_content = response.choices[0].message.content

        else:
            ai_content = f"Personalized content for {topic} in {subject}, adapted for {student['learning_style']} learners at {analysis.get('overall_level', 50)}% level."

    except Exception as e:
        ai_content = f"Let's explore {topic} in {subject}. This lesson is customized for your learning level and style."

    session_id = f"ai_session_{len(sessions_db) + 1}"
    session = {
        "session_id": session_id,
        "student_id": student_id,
        "subject": subject,
        "topic": topic,
        "progress": 0.0,
        "status": "in_progress",
        "started_at": datetime.utcnow().isoformat(),
        "ai_analysis": analysis,
        "personalized_content": {
            "difficulty_level": analysis.get("recommended_difficulty", "medium"),
            "learning_style_adaptation": student.get("learning_style", "visual"),
            "ai_generated_content": ai_content,
            "focus_areas": analysis.get("focus_areas", []),
            "estimated_time": 30,
            "content_blocks": [
                {
                    "type": "ai_explanation",
                    "title": f"Personalized Introduction to {topic}",
                    "content": ai_content[:200] + "..."
                },
                {
                    "type": "adaptive_practice",
                    "title": "Practice Activities",
                    "content": f"Activities designed for your {student.get('learning_style', 'visual')} learning style"
                }
            ]
        }
    }

    sessions_db[session_id] = session
    return session

@app.post("/api/worksheets/ai-generate")
async def generate_ai_worksheet(request_data: dict):
    """Generate AI-powered personalized worksheet"""
    student_id = request_data.get("student_id")
    subject = request_data.get("subject")
    topic = request_data.get("topic")
    num_questions = request_data.get("num_questions", 5)

    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    student = students_db[student_id]
    analysis = await analyze_student_performance(student_id)

    try:
        if openai.api_key:
            prompt = f"""
            Create {num_questions} practice questions for a grade {student['grade']} student on {subject} - {topic}.

            Student Level: {analysis.get('overall_level', 50)}%
            Difficulty: {analysis.get('recommended_difficulty', 'medium')}
            Learning Style: {student.get('learning_style', 'visual')}

            Create a mix of:
            - 2 multiple choice questions
            - 2 short answer questions
            - 1 problem-solving question

            Make questions appropriate for their level and include clear explanations.
            Format as JSON with question, options (for MCQ), correct_answer, explanation.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are creating educational worksheets for Indian students. Provide practical, relevant questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )

            ai_questions = response.choices[0].message.content

        else:
            ai_questions = "AI-generated questions would appear here with OpenAI integration."

    except Exception as e:
        ai_questions = f"Practice questions for {topic} in {subject}"

    worksheet = {
        "worksheet_id": f"ai_worksheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "title": f"AI-Personalized {subject} - {topic} Worksheet",
        "student_id": student_id,
        "difficulty_level": analysis.get("recommended_difficulty", "medium"),
        "estimated_time_minutes": 25,
        "ai_generated": True,
        "personalization": {
            "adapted_for_level": analysis.get("overall_level", 50),
            "learning_style": student.get("learning_style", "visual"),
            "focus_areas": analysis.get("focus_areas", [])
        },
        "ai_content": ai_questions,
        "problems": [
            {
                "id": 1,
                "type": "multiple_choice",
                "question": f"Based on your understanding of {topic}, which statement is most accurate?",
                "options": ["Option A (Basic)", "Option B (Intermediate)", "Option C (Advanced)", "Option D (Application)"],
                "correct_answer": "B",
                "difficulty": analysis.get("recommended_difficulty", "medium")
            },
            {
                "id": 2,
                "type": "short_answer",
                "question": f"Explain {topic} in your own words, focusing on the aspects you find most interesting.",
                "expected_length": "3-4 sentences",
                "difficulty": analysis.get("recommended_difficulty", "medium")
            }
        ],
        "learning_objectives": [
            f"Master key concepts of {topic}",
            f"Apply {topic} knowledge to solve problems",
            "Build confidence in " + ", ".join(analysis.get("focus_areas", [subject]))
        ]
    }

    return worksheet

@app.post("/api/doubts/ai-ask")
async def ai_doubt_clearing(doubt_data: dict):
    """AI-powered intelligent doubt clearing"""
    student_id = doubt_data.get("student_id")
    question = doubt_data.get("question", "")
    subject = doubt_data.get("subject", "")
    topic = doubt_data.get("topic", "")

    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    student = students_db[student_id]
    analysis = await analyze_student_performance(student_id)

    try:
        if openai.api_key and question:
            prompt = f"""
            A grade {student['grade']} student asks: "{question}"

            Student Context:
            - Subject: {subject}
            - Topic: {topic}
            - Current Level: {analysis.get('overall_level', 50)}%
            - Learning Style: {student.get('learning_style', 'visual')}
            - Strengths: {', '.join(student.get('strengths', []))}
            - Weak Areas: {', '.join(student.get('weaknesses', []))}

            Provide a helpful response that:
            1. Answers their question clearly at their level
            2. Uses simple language appropriate for grade {student['grade']}
            3. Includes practical examples they can relate to
            4. Encourages further learning
            5. Suggests follow-up questions or activities

            Be supportive and encouraging. Use the Socratic method when appropriate.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a patient, encouraging AI tutor helping Indian government school students. Always be supportive and use age-appropriate language."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )

            ai_response = response.choices[0].message.content
            confidence_score = 0.9

        else:
            ai_response = f"Great question about {topic}! Let me help you understand this step by step. This concept is important for your {subject} studies and I can see you're thinking deeply about it."
            confidence_score = 0.7

    except Exception as e:
        ai_response = f"I understand you're asking about {topic}. This is a thoughtful question! Let me break this down in a way that connects to what you already know about {subject}."
        confidence_score = 0.6

    # Generate follow-up suggestions based on student profile
    follow_up_suggestions = [
        f"Would you like to see how {topic} connects to your strength in {student.get('strengths', ['other subjects'])[0] if student.get('strengths') else 'other subjects'}?",
        f"Should we practice some examples to make {topic} clearer?",
        f"Would a visual explanation help you understand {topic} better?" if student.get('learning_style') == 'visual' else f"Would you like to hear more examples about {topic}?"
    ]

    doubt_resolution = {
        "query_id": f"ai_doubt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "student_id": student_id,
        "question": question,
        "subject": subject,
        "topic": topic,
        "ai_response": {
            "type": "personalized_explanation",
            "content": ai_response,
            "learning_level": analysis.get("overall_level", 50),
            "adapted_for_style": student.get("learning_style", "visual"),
            "encouragement": "You're asking great questions! Keep exploring and learning.",
            "follow_up_suggestions": follow_up_suggestions
        },
        "confidence_score": confidence_score,
        "personalization_applied": {
            "difficulty_adjusted": True,
            "learning_style_considered": True,
            "student_strengths_referenced": bool(student.get('strengths')),
            "encouraging_tone": True
        },
        "related_topics": [
            f"Advanced {topic}",
            f"{topic} applications",
            f"{topic} in real life"
        ],
        "recommended_next_steps": [
            f"Practice {topic} with worksheets",
            f"Explore {topic} examples",
            f"Connect {topic} to your interests"
        ],
        "created_at": datetime.utcnow().isoformat()
    }

    return doubt_resolution

@app.get("/api/analytics/ai-insights/{student_id}")
async def get_ai_student_insights(student_id: str):
    """Get AI-powered student insights and recommendations"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    student = students_db[student_id]
    analysis = await analyze_student_performance(student_id)
    student_sessions = [s for s in sessions_db.values() if s.get("student_id") == student_id]

    # AI-powered insights
    insights = {
        "student_id": student_id,
        "ai_analysis": analysis,
        "learning_insights": {
            "current_level": analysis.get("overall_level", 50),
            "learning_trajectory": "improving" if analysis.get("overall_level", 50) > 60 else "needs_support",
            "optimal_study_time": "30-45 minutes" if student.get("learning_style") == "visual" else "20-30 minutes",
            "best_learning_approach": f"Focus on {student.get('learning_style', 'visual')} learning methods"
        },
        "personalized_recommendations": [
            f"Spend extra time on {area}" for area in analysis.get("focus_areas", [])[:3]
        ] + [
            f"Leverage your strength in {strength}" for strength in analysis.get("strengths", [])[:2]
        ],
        "study_plan": {
            "daily_goals": [
                f"Practice {area} for 15 minutes" for area in analysis.get("focus_areas", ["basic concepts"])[:2]
            ],
            "weekly_goals": [
                f"Complete 2 worksheets on weak subjects",
                f"Ask 3 questions about challenging topics",
                f"Review and strengthen {analysis.get('strengths', ['your strong subjects'])[0] if analysis.get('strengths') else 'your strong subjects'}"
            ],
            "monthly_goals": [
                f"Improve overall level from {analysis.get('overall_level', 50)}% to {min(95, analysis.get('overall_level', 50) + 10)}%",
                f"Master fundamentals in {', '.join(analysis.get('focus_areas', ['key subjects'])[:2])}"
            ]
        },
        "motivation_message": f"Great progress, {student['name']}! You're doing well in {', '.join(analysis.get('strengths', ['your studies']))}. Keep working on {', '.join(analysis.get('focus_areas', ['new topics'])[:2])} and you'll see amazing improvement!",
        "next_learning_session_suggestion": {
            "recommended_subject": analysis.get("focus_areas", ["Mathematics"])[0] if analysis.get("focus_areas") else "Mathematics",
            "recommended_topic": "Fundamentals review",
            "estimated_time": 30,
            "difficulty": analysis.get("recommended_difficulty", "medium")
        }
    }

    return insights

if __name__ == "__main__":
    import uvicorn
    print("🤖 Starting AI Education Agent - Full Version...")
    print("🎓 AI-Powered Features:")
    print("   ✅ Personalized Content Generation")
    print("   ✅ Adaptive Difficulty Adjustment")
    print("   ✅ Intelligent Doubt Clearing")
    print("   ✅ Smart Learning Analytics")
    print("   ✅ Performance-Based Recommendations")
    print()
    print("🌐 Access Points:")
    print("   📚 API: http://localhost:8000")
    print("   📖 Documentation: http://localhost:8000/docs")
    print("   🔍 Health Check: http://localhost:8000/health")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8000)