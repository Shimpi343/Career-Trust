"""
Advanced NLP Service for Skill Matching
Uses NLTK and scikit-learn for better skill extraction and matching
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple

# Download required NLTK data (one-time)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)


class AdvancedSkillMatcher:
    """
    Advanced skill matching using NLP and vectorization
    """
    
    # Skill keywords with weights (higher = more important)
    TECHNICAL_SKILLS = {
        'python': 10,
        'java': 10,
        'javascript': 10,
        'typescript': 9,
        'react': 9,
        'vue': 9,
        'angular': 9,
        'node.js': 10,
        'nodejs': 10,
        'django': 8,
        'flask': 8,
        'fastapi': 8,
        'spring': 9,
        'golang': 9,
        'go': 9,
        'rust': 9,
        'csharp': 8,
        'c#': 8,
        'php': 7,
        'sql': 8,
        'mysql': 8,
        'postgresql': 8,
        'mongodb': 8,
        'redis': 7,
        'docker': 9,
        'kubernetes': 9,
        'k8s': 9,
        'aws': 9,
        'azure': 9,
        'gcp': 9,
        'git': 8,
        'linux': 8,
        'html': 6,
        'css': 6,
        'rest': 7,
        'graphql': 7,
        'api': 7,
        'machine learning': 9,
        'ml': 9,
        'ai': 9,
        'deep learning': 9,
        'tensorflow': 8,
        'pytorch': 8,
        'neural network': 8,
        'nlp': 8,
        'data science': 8,
        'pandas': 7,
        'numpy': 7,
        'scikit-learn': 7,
        'hadoop': 8,
        'spark': 8,
        'kafka': 8,
        'elasticsearch': 7,
    }
    
    @staticmethod
    def extract_skills_nlp(text: str) -> List[str]:
        """
        Extract skills using NLP techniques
        
        Args:
            text: Job description or resume text
        
        Returns:
            List of detected skills
        """
        if not text:
            return []
        
        text_lower = text.lower()
        detected_skills = set()
        
        # Check for technical skills
        for skill, weight in AdvancedSkillMatcher.TECHNICAL_SKILLS.items():
            # Use word boundaries for better matching
            import re
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                detected_skills.add(skill)
        
        return list(detected_skills)
    
    @staticmethod
    def calculate_tfidf_similarity(user_skills: List[str], job_description: str) -> float:
        """
        Calculate similarity using TF-IDF vectorization
        
        Args:
            user_skills: List of user skills
            job_description: Job description text
        
        Returns:
            Similarity score (0-1)
        """
        try:
            if not user_skills or not job_description:
                return 0.0
            
            # Create documents
            user_doc = " ".join(user_skills)
            documents = [user_doc, job_description]
            
            # Vectorize
            vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"TF-IDF similarity error: {e}")
            return 0.0
    
    @staticmethod
    def rank_jobs_advanced(jobs: List[Dict], user_skills: List[str]) -> List[Dict]:
        """
        Rank jobs using advanced NLP techniques
        
        Args:
            jobs: List of job dictionaries
            user_skills: User's skills
        
        Returns:
            Ranked list of jobs with advanced scores
        """
        scored_jobs = []
        
        for job in jobs:
            description = f"{job.get('title', '')} {job.get('description', '')}"
            
            # Extract skills from job description
            job_skills = AdvancedSkillMatcher.extract_skills_nlp(description)
            
            # Calculate match using intersection
            matched = list(set(user_skills) & set(job_skills))
            missing = list(set(user_skills) - set(job_skills))
            
            # Basic match score
            if job_skills:
                basic_match = (len(matched) / len(job_skills)) * 100
            else:
                basic_match = 0
            
            # TF-IDF similarity score (0-100)
            tfidf_score = AdvancedSkillMatcher.calculate_tfidf_similarity(user_skills, description) * 100
            
            # Combined score (weight basic match more heavily)
            combined_score = (basic_match * 0.6) + (tfidf_score * 0.4)
            
            job_with_score = job.copy()
            job_with_score['match_score'] = round(combined_score, 1)
            job_with_score['matched_skills'] = matched
            job_with_score['missing_skills'] = missing
            job_with_score['job_skills_found'] = job_skills
            
            scored_jobs.append(job_with_score)
        
        # Sort by score
        ranked = sorted(
            scored_jobs,
            key=lambda x: (x.get('match_score', 0), x.get('trust_score', 0)),
            reverse=True
        )
        
        return ranked


class ResumeAnalyzer:
    """
    Analyze resume for skills, experience, and education
    """
    
    @staticmethod
    def extract_experience_level(resume_text: str) -> int:
        """
        Estimate years of experience from resume
        
        Args:
            resume_text: Resume content
        
        Returns:
            Estimated years of experience
        """
        import re
        
        text_lower = resume_text.lower()
        
        # Look for year patterns
        year_pattern = r'(\d{1,2})\s*\+?\s*years?'
        matches = re.findall(year_pattern, text_lower)
        
        if matches:
            # Return average or take the explicit mention
            years = [int(m) for m in matches]
            return min(max(years), 50)  # Cap at 50 years max
        
        return 0
    
    @staticmethod
    def extract_education(resume_text: str) -> List[str]:
        """
        Extract education keywords from resume
        
        Args:
            resume_text: Resume content
        
        Returns:
            List of education keywords
        """
        education_keywords = [
            'bachelor', 'bs', 'b.s.',
            'master', 'ms', 'm.s.',
            'phd', 'ph.d.',
            'diploma',
            'computer science', 'engineering',
            'mathematics', 'statistics',
            'business', 'economics'
        ]
        
        text_lower = resume_text.lower()
        found_education = []
        
        for keyword in education_keywords:
            if keyword in text_lower:
                found_education.append(keyword)
        
        return found_education
