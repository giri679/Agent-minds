"""
Worksheet Generator - AI Component for Adaptive Content Creation
Generates personalized worksheets based on student's learning profile and curriculum
"""

import openai
import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re

class WorksheetGenerator:
    """
    AI-powered worksheet generator that creates personalized practice materials
    based on student's learning profile, difficulty level, and curriculum requirements
    """

    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.question_templates = self._load_question_templates()
        self.curriculum_standards = self._load_curriculum_standards()

    def generate_worksheet(self,
                          student_profile: Dict,
                          subject: str,
                          topic: str,
                          difficulty_level: int = 3,
                          num_questions: int = 10,
                          question_types: List[str] = None) -> Dict:
        """
        Generate a personalized worksheet for a student

        Args:
            student_profile: Student's learning profile and preferences
            subject: Subject area (e.g., "Mathematics", "Science")
            topic: Specific topic within the subject
            difficulty_level: Difficulty level (1-5 scale)
            num_questions: Number of questions to generate
            question_types: Types of questions to include

        Returns:
            Dictionary containing the generated worksheet
        """
        if question_types is None:
            question_types = ["multiple_choice", "short_answer", "problem_solving"]

        # Analyze student profile for personalization
        personalization_config = self._extract_personalization_config(student_profile)

        # Generate questions based on curriculum and student needs
        questions = self._generate_questions(
            subject=subject,
            topic=topic,
            difficulty_level=difficulty_level,
            num_questions=num_questions,
            question_types=question_types,
            personalization_config=personalization_config
        )

        # Create worksheet structure
        worksheet = {
            "id": f"worksheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": f"{subject} - {topic} Practice Worksheet",
            "subject": subject,
            "topic": topic,
            "difficulty_level": difficulty_level,
            "estimated_time_minutes": self._estimate_completion_time(questions),
            "instructions": self._generate_instructions(personalization_config),
            "questions": questions,
            "learning_objectives": self._generate_learning_objectives(subject, topic),
            "personalization_applied": personalization_config,
            "created_at": datetime.utcnow().isoformat()
        }

        return worksheet

    def _generate_questions(self,
                           subject: str,
                           topic: str,
                           difficulty_level: int,
                           num_questions: int,
                           question_types: List[str],
                           personalization_config: Dict) -> List[Dict]:
        """Generate questions using AI and templates"""
        questions = []

        # Distribute questions across types
        type_distribution = self._distribute_question_types(question_types, num_questions)

        for question_type, count in type_distribution.items():
            for i in range(count):
                question = self._generate_single_question(
                    subject=subject,
                    topic=topic,
                    question_type=question_type,
                    difficulty_level=difficulty_level,
                    personalization_config=personalization_config,
                    question_number=len(questions) + 1
                )
                questions.append(question)

        return questions

    def _generate_single_question(self,
                                 subject: str,
                                 topic: str,
                                 question_type: str,
                                 difficulty_level: int,
                                 personalization_config: Dict,
                                 question_number: int) -> Dict:
        """Generate a single question using AI"""

        # Create prompt for AI generation
        prompt = self._create_question_prompt(
            subject=subject,
            topic=topic,
            question_type=question_type,
            difficulty_level=difficulty_level,
            personalization_config=personalization_config
        )

        try:
            # Use OpenAI to generate question
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert educator creating personalized questions for government school students."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            question_data = self._parse_ai_response(response.choices[0].message.content)

        except Exception as e:
            # Fallback to template-based generation
            question_data = self._generate_from_template(
                subject, topic, question_type, difficulty_level
            )

        # Add metadata
        question_data.update({
            "id": question_number,
            "subject": subject,
            "topic": topic,
            "difficulty_level": difficulty_level,
            "question_type": question_type,
            "estimated_time_minutes": self._estimate_question_time(question_type, difficulty_level)
        })

        return question_data

    def _create_question_prompt(self,
                               subject: str,
                               topic: str,
                               question_type: str,
                               difficulty_level: int,
                               personalization_config: Dict) -> str:
        """Create AI prompt for question generation"""

        learning_style = personalization_config.get("learning_style", "visual")
        language_level = personalization_config.get("language_level", "grade_appropriate")

        base_prompt = f"""
        Create a {question_type} question for {subject} on the topic of {topic}.

        Requirements:
        - Difficulty level: {difficulty_level}/5 (1=very easy, 5=very challenging)
        - Learning style: {learning_style}
        - Language level: {language_level}
        - Suitable for government school students
        - Include clear instructions
        - Provide correct answer and explanation
        """

        if question_type == "multiple_choice":
            base_prompt += """
            Format as JSON:
            {
                "question": "Question text",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "A",
                "explanation": "Why this answer is correct",
                "distractors_explanation": "Why other options are incorrect"
            }
            """
        elif question_type == "short_answer":
            base_prompt += """
            Format as JSON:
            {
                "question": "Question text",
                "sample_answer": "Expected answer",
                "key_points": ["point1", "point2", "point3"],
                "explanation": "Detailed explanation"
            }
            """
        elif question_type == "problem_solving":
            base_prompt += """
            Format as JSON:
            {
                "question": "Problem statement",
                "solution_steps": ["step1", "step2", "step3"],
                "final_answer": "Final answer",
                "explanation": "Step-by-step explanation"
            }
            """

        # Add personalization based on learning style
        if learning_style == "visual":
            base_prompt += "\n- Include visual elements or diagrams when possible"
        elif learning_style == "kinesthetic":
            base_prompt += "\n- Include hands-on or practical applications"
        elif learning_style == "auditory":
            base_prompt += "\n- Include verbal explanations and discussions"

        return base_prompt