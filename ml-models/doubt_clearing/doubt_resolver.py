"""
Doubt Resolver - AI Component for Intelligent Tutoring
Provides personalized doubt clearing and explanations using AI
"""

import openai
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize

class DoubtResolver:
    """
    AI-powered doubt resolver that provides personalized explanations,
    examples, and guidance for student questions
    """

    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.common_misconceptions = self._load_common_misconceptions()
        self.explanation_templates = self._load_explanation_templates()

    def resolve_doubt(self,
                     question: str,
                     student_profile: Dict,
                     context: Optional[str] = None,
                     subject: Optional[str] = None,
                     topic: Optional[str] = None) -> Dict:
        """
        Resolve a student's doubt with personalized explanation

        Args:
            question: Student's question or doubt
            student_profile: Student's learning profile
            context: Additional context about what student was studying
            subject: Subject area of the question
            topic: Specific topic within the subject

        Returns:
            Dictionary containing AI response and metadata
        """

        # Analyze the question
        question_analysis = self._analyze_question(question, subject, topic)

        # Determine response strategy
        response_strategy = self._determine_response_strategy(
            question_analysis, student_profile
        )

        # Generate personalized response
        ai_response = self._generate_response(
            question=question,
            context=context,
            question_analysis=question_analysis,
            student_profile=student_profile,
            response_strategy=response_strategy
        )

        # Create response structure
        doubt_resolution = {
            "query_id": f"doubt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "question": question,
            "subject": subject,
            "topic": topic,
            "context": context,
            "question_analysis": question_analysis,
            "response": ai_response,
            "confidence_score": self._calculate_confidence_score(question_analysis, ai_response),
            "follow_up_suggestions": self._generate_follow_up_suggestions(question_analysis),
            "related_topics": self._identify_related_topics(question_analysis),
            "difficulty_level": question_analysis.get("difficulty_level", "medium"),
            "response_strategy": response_strategy,
            "created_at": datetime.utcnow().isoformat()
        }

        return doubt_resolution

    def _analyze_question(self, question: str, subject: Optional[str], topic: Optional[str]) -> Dict:
        """Analyze the student's question to understand intent and complexity"""

        analysis = {
            "question_type": self._classify_question_type(question),
            "complexity_level": self._assess_complexity(question),
            "key_concepts": self._extract_key_concepts(question, subject),
            "sentiment": self._analyze_sentiment(question),
            "misconception_indicators": self._detect_misconceptions(question),
            "urgency_level": self._assess_urgency(question)
        }

        return analysis

    def _classify_question_type(self, question: str) -> str:
        """Classify the type of question being asked"""

        question_lower = question.lower()

        # Question type patterns
        if any(word in question_lower for word in ["what", "define", "meaning"]):
            return "definition"
        elif any(word in question_lower for word in ["how", "steps", "process"]):
            return "procedure"
        elif any(word in question_lower for word in ["why", "reason", "because"]):
            return "explanation"
        elif any(word in question_lower for word in ["example", "instance", "show me"]):
            return "example_request"
        elif any(word in question_lower for word in ["solve", "calculate", "find"]):
            return "problem_solving"
        elif any(word in question_lower for word in ["difference", "compare", "versus"]):
            return "comparison"
        else:
            return "general_inquiry"

    def _assess_complexity(self, question: str) -> str:
        """Assess the complexity level of the question"""

        # Simple heuristics for complexity assessment
        word_count = len(question.split())
        technical_terms = self._count_technical_terms(question)

        if word_count < 10 and technical_terms < 2:
            return "simple"
        elif word_count < 20 and technical_terms < 4:
            return "medium"
        else:
            return "complex"

    def _extract_key_concepts(self, question: str, subject: Optional[str]) -> List[str]:
        """Extract key concepts from the question"""

        # Tokenize and extract important terms
        tokens = word_tokenize(question.lower())

        # Remove common words and extract potential concepts
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        concepts = [token for token in tokens if token not in stop_words and len(token) > 3]

        # Subject-specific concept extraction could be enhanced with domain knowledge
        return concepts[:5]  # Return top 5 concepts

    def _analyze_sentiment(self, question: str) -> Dict:
        """Analyze the emotional tone of the question"""

        scores = self.sentiment_analyzer.polarity_scores(question)

        # Determine primary emotion
        if scores['compound'] <= -0.5:
            emotion = "frustrated"
        elif scores['compound'] >= 0.5:
            emotion = "curious"
        elif scores['neu'] > 0.7:
            emotion = "neutral"
        else:
            emotion = "confused"

        return {
            "emotion": emotion,
            "confidence": abs(scores['compound']),
            "scores": scores
        }

    def _detect_misconceptions(self, question: str) -> List[str]:
        """Detect potential misconceptions in the question"""

        misconceptions = []
        question_lower = question.lower()

        # Check against common misconception patterns
        for misconception, patterns in self.common_misconceptions.items():
            for pattern in patterns:
                if pattern in question_lower:
                    misconceptions.append(misconception)
                    break

        return misconceptions

    def _assess_urgency(self, question: str) -> str:
        """Assess the urgency level of the question"""

        urgent_indicators = ["urgent", "exam", "test", "tomorrow", "help", "stuck", "confused"]
        question_lower = question.lower()

        urgent_count = sum(1 for indicator in urgent_indicators if indicator in question_lower)

        if urgent_count >= 2:
            return "high"
        elif urgent_count == 1:
            return "medium"
        else:
            return "low"

    def _determine_response_strategy(self, question_analysis: Dict, student_profile: Dict) -> Dict:
        """Determine the best strategy for responding to the question"""

        learning_style = student_profile.get("learning_style", "visual")
        difficulty_level = student_profile.get("current_level", 50)

        strategy = {
            "approach": "socratic",  # socratic, direct, guided
            "explanation_style": "detailed",  # brief, detailed, step_by_step
            "include_examples": True,
            "use_analogies": False,
            "provide_practice": False
        }

        # Adjust based on question type
        question_type = question_analysis.get("question_type", "general_inquiry")

        if question_type == "definition":
            strategy["approach"] = "direct"
            strategy["explanation_style"] = "detailed"
        elif question_type == "procedure":
            strategy["explanation_style"] = "step_by_step"
            strategy["include_examples"] = True
        elif question_type == "explanation":
            strategy["approach"] = "socratic"
            strategy["use_analogies"] = True

        # Adjust based on learning style
        if learning_style == "visual":
            strategy["include_diagrams"] = True
        elif learning_style == "kinesthetic":
            strategy["provide_practice"] = True

        # Adjust based on complexity and student level
        complexity = question_analysis.get("complexity_level", "medium")
        if complexity == "complex" and difficulty_level < 70:
            strategy["explanation_style"] = "step_by_step"
            strategy["use_analogies"] = True

        return strategy