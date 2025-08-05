"""
Database Models for AI Education Agent
Defines the core data structures for students, curriculum, assessments, and learning analytics
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Student(Base):
    """Student profile with academic history and learning preferences"""
    __tablename__ = "students"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, unique=True, nullable=False)  # Government student ID
    name = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)
    school_id = Column(String, nullable=False)
    date_of_birth = Column(DateTime)
    language_preference = Column(String, default="english")

    # Learning profile
    learning_style = Column(String)  # visual, auditory, kinesthetic
    current_level = Column(Float, default=0.0)  # Overall competency level (0-100)
    strengths = Column(JSON)  # List of strong subjects/topics
    weaknesses = Column(JSON)  # List of areas needing improvement

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    academic_records = relationship("AcademicRecord", back_populates="student")
    learning_sessions = relationship("LearningSession", back_populates="student")
    assessments = relationship("Assessment", back_populates="student")
    doubt_queries = relationship("DoubtQuery", back_populates="student")

class AcademicRecord(Base):
    """Historical academic performance data"""
    __tablename__ = "academic_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    subject = Column(String, nullable=False)
    topic = Column(String)
    grade_level = Column(Integer, nullable=False)

    # Performance metrics
    score = Column(Float, nullable=False)  # Percentage score
    max_score = Column(Float, nullable=False)
    assessment_type = Column(String)  # exam, quiz, assignment, project
    difficulty_level = Column(String)  # easy, medium, hard

    # Temporal data
    assessment_date = Column(DateTime, nullable=False)
    academic_year = Column(String, nullable=False)
    semester = Column(String)

    # Analysis
    time_taken_minutes = Column(Integer)
    attempts = Column(Integer, default=1)
    concepts_covered = Column(JSON)  # List of concepts tested

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="academic_records")

class Curriculum(Base):
    """Government curriculum structure and learning objectives"""
    __tablename__ = "curriculum"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)
    chapter = Column(String, nullable=False)
    topic = Column(String, nullable=False)

    # Learning objectives
    learning_objectives = Column(JSON)  # List of specific learning goals
    prerequisites = Column(JSON)  # Required prior knowledge
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    estimated_hours = Column(Float)  # Expected learning time

    # Content metadata
    content_type = Column(String)  # theory, practical, mixed
    keywords = Column(JSON)  # Searchable keywords
    government_standard_code = Column(String)  # Official curriculum code

    # Relationships
    content_items = relationship("ContentItem", back_populates="curriculum")
    learning_sessions = relationship("LearningSession", back_populates="curriculum")

class ContentItem(Base):
    """Learning content and materials"""
    __tablename__ = "content_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_id = Column(String, ForeignKey("curriculum.id"), nullable=False)
    title = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # explanation, example, exercise, video

    # Content data
    content_text = Column(Text)
    content_html = Column(Text)
    multimedia_url = Column(String)
    difficulty_level = Column(Integer, default=1)

    # Personalization metadata
    learning_style_tags = Column(JSON)  # visual, auditory, kinesthetic
    language = Column(String, default="english")
    reading_level = Column(Integer)  # Grade level for text complexity

    # Usage tracking
    view_count = Column(Integer, default=0)
    effectiveness_score = Column(Float, default=0.0)  # Based on student outcomes

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    curriculum = relationship("Curriculum", back_populates="content_items")

class LearningSession(Base):
    """Individual learning sessions and progress tracking"""
    __tablename__ = "learning_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    curriculum_id = Column(String, ForeignKey("curriculum.id"), nullable=False)

    # Session details
    session_type = Column(String, nullable=False)  # lesson, practice, assessment, doubt_clearing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)

    # Progress metrics
    completion_percentage = Column(Float, default=0.0)
    comprehension_score = Column(Float)  # AI-assessed understanding level
    engagement_score = Column(Float)  # Based on interaction patterns

    # Learning data
    concepts_covered = Column(JSON)
    mistakes_made = Column(JSON)  # Common errors for analysis
    help_requests = Column(Integer, default=0)

    # Adaptive learning
    difficulty_adjustments = Column(JSON)  # Track difficulty changes during session
    personalization_applied = Column(JSON)  # What personalizations were used

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="learning_sessions")
    curriculum = relationship("Curriculum", back_populates="learning_sessions")
    worksheets = relationship("Worksheet", back_populates="learning_session")

class Assessment(Base):
    """Assessments and quizzes for measuring student progress"""
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    curriculum_id = Column(String, ForeignKey("curriculum.id"))

    # Assessment details
    title = Column(String, nullable=False)
    assessment_type = Column(String, nullable=False)  # diagnostic, formative, summative
    questions = Column(JSON, nullable=False)  # List of questions with options and correct answers

    # Results
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0)
    score_percentage = Column(Float, default=0.0)
    time_taken_minutes = Column(Integer)

    # Analysis
    concept_scores = Column(JSON)  # Performance by concept/topic
    difficulty_analysis = Column(JSON)  # Performance by difficulty level
    learning_gaps = Column(JSON)  # Identified areas for improvement

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    is_completed = Column(Boolean, default=False)

    # Relationships
    student = relationship("Student", back_populates="assessments")

class Worksheet(Base):
    """AI-generated worksheets for practice"""
    __tablename__ = "worksheets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    learning_session_id = Column(String, ForeignKey("learning_sessions.id"))
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    curriculum_id = Column(String, ForeignKey("curriculum.id"), nullable=False)

    # Worksheet details
    title = Column(String, nullable=False)
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    estimated_time_minutes = Column(Integer)

    # Content
    problems = Column(JSON, nullable=False)  # List of problems with solutions
    instructions = Column(Text)
    learning_objectives = Column(JSON)

    # Personalization
    adapted_for_learning_style = Column(String)
    language = Column(String, default="english")
    complexity_level = Column(String)  # simplified, standard, advanced

    # Progress tracking
    completion_status = Column(String, default="not_started")  # not_started, in_progress, completed
    student_answers = Column(JSON)  # Student's submitted answers
    score = Column(Float)
    feedback = Column(Text)  # AI-generated feedback

    # Metadata
    generated_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    learning_session = relationship("LearningSession", back_populates="worksheets")

class DoubtQuery(Base):
    """Student questions and AI responses for doubt clearing"""
    __tablename__ = "doubt_queries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    curriculum_id = Column(String, ForeignKey("curriculum.id"))

    # Query details
    question = Column(Text, nullable=False)
    context = Column(Text)  # Additional context about what student was studying
    subject = Column(String)
    topic = Column(String)

    # AI Response
    ai_response = Column(Text)
    response_type = Column(String)  # explanation, example, hint, question
    confidence_score = Column(Float)  # AI confidence in response quality

    # Interaction data
    student_satisfaction = Column(Integer)  # 1-5 rating from student
    follow_up_questions = Column(JSON)  # Additional questions asked
    resolution_status = Column(String, default="pending")  # pending, resolved, escalated

    # Learning analytics
    concept_tags = Column(JSON)  # Concepts related to the doubt
    difficulty_level = Column(String)
    common_misconception = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

    # Relationships
    student = relationship("Student", back_populates="doubt_queries")

class TeacherProfile(Base):
    """Teacher profiles and their classes"""
    __tablename__ = "teachers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    school_id = Column(String, nullable=False)

    # Professional details
    subjects_taught = Column(JSON)  # List of subjects
    grades_taught = Column(JSON)  # List of grade levels
    experience_years = Column(Integer)
    qualifications = Column(JSON)

    # System access
    role = Column(String, default="teacher")  # teacher, head_teacher, admin
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)

    # Preferences
    dashboard_preferences = Column(JSON)
    notification_settings = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LearningAnalytics(Base):
    """Aggregated analytics and insights"""
    __tablename__ = "learning_analytics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"))
    school_id = Column(String)
    grade = Column(Integer)
    subject = Column(String)

    # Time period
    analysis_period = Column(String, nullable=False)  # daily, weekly, monthly, yearly
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)

    # Metrics
    total_learning_time_minutes = Column(Integer, default=0)
    sessions_completed = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    improvement_rate = Column(Float, default=0.0)  # Rate of improvement over time

    # Engagement metrics
    login_frequency = Column(Integer, default=0)
    content_interaction_score = Column(Float, default=0.0)
    help_seeking_frequency = Column(Integer, default=0)

    # Learning outcomes
    concepts_mastered = Column(JSON)  # List of mastered concepts
    learning_goals_achieved = Column(JSON)
    areas_for_improvement = Column(JSON)

    # Predictions
    predicted_performance = Column(Float)  # AI prediction for future performance
    risk_level = Column(String)  # low, medium, high (risk of falling behind)
    recommended_interventions = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)