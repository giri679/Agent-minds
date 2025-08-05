"""
Student Profiler - AI Component for Personalized Learning
Analyzes student's academic history and creates personalized learning profiles
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime, timedelta

class StudentProfiler:
    """
    AI-powered student profiler that analyzes academic history and learning patterns
    to create personalized learning recommendations
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=5)
        self.learning_style_classifier = None
        self.difficulty_predictor = None

    def analyze_academic_history(self, academic_records: List[Dict]) -> Dict:
        """
        Analyze student's academic performance history to identify patterns

        Args:
            academic_records: List of academic performance records

        Returns:
            Dict containing analysis results and insights
        """
        if not academic_records:
            return self._default_profile()

        df = pd.DataFrame(academic_records)

        # Calculate performance metrics
        overall_performance = self._calculate_overall_performance(df)
        subject_strengths = self._identify_subject_strengths(df)
        learning_trends = self._analyze_learning_trends(df)
        difficulty_preferences = self._assess_difficulty_preferences(df)

        return {
            "overall_performance": overall_performance,
            "subject_strengths": subject_strengths,
            "learning_trends": learning_trends,
            "difficulty_preferences": difficulty_preferences,
            "recommended_level": self._recommend_difficulty_level(df),
            "learning_gaps": self._identify_learning_gaps(df),
            "study_patterns": self._analyze_study_patterns(df)
        }

    def _calculate_overall_performance(self, df: pd.DataFrame) -> Dict:
        """Calculate overall academic performance metrics"""
        return {
            "average_score": float(df['score'].mean()),
            "score_std": float(df['score'].std()),
            "improvement_rate": self._calculate_improvement_rate(df),
            "consistency_score": self._calculate_consistency(df),
            "recent_performance": float(df.tail(5)['score'].mean()) if len(df) >= 5 else float(df['score'].mean())
        }

    def _identify_subject_strengths(self, df: pd.DataFrame) -> Dict:
        """Identify subjects where student performs well"""
        subject_performance = df.groupby('subject')['score'].agg(['mean', 'count', 'std']).reset_index()
        subject_performance['weighted_score'] = (
            subject_performance['mean'] * np.log(subject_performance['count'] + 1)
        )

        # Sort by weighted performance
        subject_performance = subject_performance.sort_values('weighted_score', ascending=False)

        strengths = subject_performance.head(3)['subject'].tolist()
        weaknesses = subject_performance.tail(2)['subject'].tolist()

        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "subject_scores": subject_performance[['subject', 'mean']].to_dict('records')
        }

    def _analyze_learning_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze learning trends over time"""
        df['assessment_date'] = pd.to_datetime(df['assessment_date'])
        df = df.sort_values('assessment_date')

        # Calculate rolling averages
        df['rolling_avg'] = df['score'].rolling(window=5, min_periods=1).mean()

        # Trend analysis
        recent_trend = self._calculate_trend(df.tail(10)['score'].values)
        overall_trend = self._calculate_trend(df['score'].values)

        return {
            "recent_trend": recent_trend,
            "overall_trend": overall_trend,
            "volatility": float(df['score'].std()),
            "peak_performance": float(df['score'].max()),
            "lowest_performance": float(df['score'].min())
        }

    def _assess_difficulty_preferences(self, df: pd.DataFrame) -> Dict:
        """Assess student's performance across different difficulty levels"""
        if 'difficulty_level' not in df.columns:
            return {"optimal_difficulty": "medium", "difficulty_scores": {}}

        difficulty_performance = df.groupby('difficulty_level')['score'].mean()

        # Find optimal difficulty (best performance with reasonable challenge)
        optimal_difficulty = self._find_optimal_difficulty(difficulty_performance)

        return {
            "optimal_difficulty": optimal_difficulty,
            "difficulty_scores": difficulty_performance.to_dict(),
            "challenge_tolerance": self._calculate_challenge_tolerance(df)
        }

    def _recommend_difficulty_level(self, df: pd.DataFrame) -> int:
        """Recommend appropriate difficulty level (1-5 scale)"""
        avg_score = df['score'].mean()
        recent_performance = df.tail(5)['score'].mean() if len(df) >= 5 else avg_score
        improvement_rate = self._calculate_improvement_rate(df)

        # Base difficulty on performance and improvement
        if recent_performance >= 85 and improvement_rate > 0:
            return min(5, int((recent_performance - 60) / 10) + 1)
        elif recent_performance >= 70:
            return max(2, int((recent_performance - 50) / 15))
        else:
            return 1

    def _identify_learning_gaps(self, df: pd.DataFrame) -> List[Dict]:
        """Identify specific learning gaps and areas for improvement"""
        gaps = []

        # Subject-wise gaps
        subject_performance = df.groupby('subject')['score'].mean()
        weak_subjects = subject_performance[subject_performance < 70].index.tolist()

        for subject in weak_subjects:
            subject_data = df[df['subject'] == subject]
            if 'topic' in subject_data.columns:
                weak_topics = subject_data.groupby('topic')['score'].mean()
                weak_topics = weak_topics[weak_topics < 65].index.tolist()

                gaps.append({
                    "subject": subject,
                    "weak_topics": weak_topics,
                    "average_score": float(subject_performance[subject]),
                    "priority": "high" if subject_performance[subject] < 60 else "medium"
                })

        return gaps

    def _analyze_study_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze study patterns and learning behavior"""
        patterns = {}

        if 'time_taken_minutes' in df.columns:
            patterns['average_study_time'] = float(df['time_taken_minutes'].mean())
            patterns['study_time_consistency'] = float(df['time_taken_minutes'].std())

        if 'attempts' in df.columns:
            patterns['average_attempts'] = float(df['attempts'].mean())
            patterns['persistence_score'] = self._calculate_persistence_score(df)

        # Performance by assessment type
        if 'assessment_type' in df.columns:
            type_performance = df.groupby('assessment_type')['score'].mean()
            patterns['assessment_type_preferences'] = type_performance.to_dict()

        return patterns

    def predict_learning_style(self, interaction_data: Dict) -> str:
        """
        Predict student's learning style based on interaction patterns

        Args:
            interaction_data: Dictionary containing interaction metrics

        Returns:
            Predicted learning style: 'visual', 'auditory', or 'kinesthetic'
        """
        # Simple heuristic-based prediction (can be replaced with ML model)
        visual_score = interaction_data.get('image_interactions', 0) + \
                      interaction_data.get('diagram_time', 0) * 0.1

        auditory_score = interaction_data.get('audio_interactions', 0) + \
                        interaction_data.get('explanation_requests', 0) * 0.5

        kinesthetic_score = interaction_data.get('interactive_exercises', 0) + \
                           interaction_data.get('hands_on_activities', 0) * 0.3

        scores = {
            'visual': visual_score,
            'auditory': auditory_score,
            'kinesthetic': kinesthetic_score
        }

        return max(scores, key=scores.get)

    def generate_personalization_config(self, student_profile: Dict) -> Dict:
        """
        Generate personalization configuration based on student profile

        Args:
            student_profile: Complete student profile with analysis

        Returns:
            Configuration for personalizing content and difficulty
        """
        config = {
            "difficulty_level": student_profile.get("recommended_level", 3),
            "learning_style": student_profile.get("learning_style", "visual"),
            "content_preferences": self._determine_content_preferences(student_profile),
            "pacing": self._determine_optimal_pacing(student_profile),
            "support_level": self._determine_support_level(student_profile),
            "motivation_strategy": self._determine_motivation_strategy(student_profile)
        }

        return config

    # Helper methods
    def _default_profile(self) -> Dict:
        """Return default profile for new students"""
        return {
            "overall_performance": {"average_score": 50.0, "improvement_rate": 0.0},
            "subject_strengths": {"strengths": [], "weaknesses": []},
            "learning_trends": {"recent_trend": "stable", "overall_trend": "stable"},
            "difficulty_preferences": {"optimal_difficulty": "medium"},
            "recommended_level": 2,
            "learning_gaps": [],
            "study_patterns": {}
        }

    def _calculate_improvement_rate(self, df: pd.DataFrame) -> float:
        """Calculate rate of improvement over time"""
        if len(df) < 2:
            return 0.0

        df_sorted = df.sort_values('assessment_date')
        recent_scores = df_sorted.tail(5)['score'].mean()
        older_scores = df_sorted.head(5)['score'].mean()

        return float((recent_scores - older_scores) / max(older_scores, 1))

    def _calculate_consistency(self, df: pd.DataFrame) -> float:
        """Calculate consistency score (lower std = higher consistency)"""
        std_score = df['score'].std()
        return float(max(0, 100 - std_score))

    def _calculate_trend(self, scores: np.ndarray) -> str:
        """Calculate trend direction from scores"""
        if len(scores) < 2:
            return "stable"

        # Simple linear regression slope
        x = np.arange(len(scores))
        slope = np.polyfit(x, scores, 1)[0]

        if slope > 2:
            return "improving"
        elif slope < -2:
            return "declining"
        else:
            return "stable"

    def _find_optimal_difficulty(self, difficulty_performance: pd.Series) -> str:
        """Find optimal difficulty level based on performance"""
        if difficulty_performance.empty:
            return "medium"

        # Find difficulty with best performance above 70%
        good_performance = difficulty_performance[difficulty_performance >= 70]
        if not good_performance.empty:
            return good_performance.idxmax()

        # Otherwise, return difficulty with best performance
        return difficulty_performance.idxmax()

    def _calculate_challenge_tolerance(self, df: pd.DataFrame) -> float:
        """Calculate how well student handles challenging content"""
        if 'difficulty_level' not in df.columns:
            return 0.5

        hard_problems = df[df['difficulty_level'].isin(['hard', 'very_hard'])]
        if hard_problems.empty:
            return 0.5

        return float(hard_problems['score'].mean() / 100)

    def _calculate_persistence_score(self, df: pd.DataFrame) -> float:
        """Calculate persistence based on attempts and completion"""
        if 'attempts' not in df.columns:
            return 0.5

        avg_attempts = df['attempts'].mean()
        # Higher attempts with eventual success indicates persistence
        successful_attempts = df[df['score'] >= 60]['attempts'].mean()

        return float(min(1.0, successful_attempts / max(avg_attempts, 1)))

    def _determine_content_preferences(self, profile: Dict) -> Dict:
        """Determine content preferences based on profile"""
        preferences = {
            "explanation_style": "detailed",
            "example_types": ["practical", "visual"],
            "interaction_level": "medium"
        }

        # Adjust based on learning style
        learning_style = profile.get("learning_style", "visual")
        if learning_style == "visual":
            preferences["example_types"] = ["visual", "diagrams", "charts"]
        elif learning_style == "auditory":
            preferences["example_types"] = ["verbal", "audio", "discussions"]
        elif learning_style == "kinesthetic":
            preferences["example_types"] = ["hands-on", "interactive", "practical"]

        return preferences

    def _determine_optimal_pacing(self, profile: Dict) -> Dict:
        """Determine optimal learning pace"""
        study_patterns = profile.get("study_patterns", {})
        avg_study_time = study_patterns.get("average_study_time", 30)

        if avg_study_time < 20:
            return {"pace": "fast", "session_length": 15, "break_frequency": 10}
        elif avg_study_time > 45:
            return {"pace": "slow", "session_length": 60, "break_frequency": 20}
        else:
            return {"pace": "medium", "session_length": 30, "break_frequency": 15}

    def _determine_support_level(self, profile: Dict) -> str:
        """Determine level of support needed"""
        overall_perf = profile.get("overall_performance", {})
        avg_score = overall_perf.get("average_score", 50)

        if avg_score < 60:
            return "high"
        elif avg_score < 75:
            return "medium"
        else:
            return "low"

    def _determine_motivation_strategy(self, profile: Dict) -> Dict:
        """Determine motivation strategy based on profile"""
        learning_trends = profile.get("learning_trends", {})
        recent_trend = learning_trends.get("recent_trend", "stable")

        if recent_trend == "declining":
            return {
                "strategy": "encouragement",
                "focus": "small_wins",
                "rewards": "frequent"
            }
        elif recent_trend == "improving":
            return {
                "strategy": "challenge",
                "focus": "growth",
                "rewards": "achievement_based"
            }
        else:
            return {
                "strategy": "balanced",
                "focus": "consistency",
                "rewards": "progress_based"
            }