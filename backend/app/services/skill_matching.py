"""
Skill Matching Service
Matches user skills to job requirements and calculates match percentages
"""

from typing import List, Dict, Tuple
import re
from difflib import SequenceMatcher

# Common skill categories for normalization
SKILL_ALIASES = {
    'python': ['python', 'py'],
    'javascript': ['javascript', 'js', 'node.js', 'nodejs'],
    'react': ['react', 'reactjs'],
    'vue': ['vue', 'vuejs', 'vue.js'],
    'angular': ['angular', 'angularjs'],
    'typescript': ['typescript', 'ts'],
    'java': ['java'],
    'csharp': ['c#', 'c sharp', 'csharp', '.net'],
    'php': ['php'],
    'golang': ['go', 'golang'],
    'rust': ['rust'],
    'swift': ['swift'],
    'kotlin': ['kotlin'],
    'sql': ['sql', 'mysql', 'postgresql', 'postgres', 'oracle'],
    'mongodb': ['mongodb', 'mongo'],
    'aws': ['aws', 'amazon web services'],
    'azure': ['azure', 'microsoft azure'],
    'gcp': ['gcp', 'google cloud', 'google cloud platform'],
    'docker': ['docker'],
    'kubernetes': ['kubernetes', 'k8s'],
    'git': ['git', 'github', 'gitlab'],
    'linux': ['linux', 'ubuntu'],
    'html': ['html', 'html5'],
    'css': ['css', 'sass', 'scss'],
    'rest api': ['rest', 'rest api', 'restful'],
    'graphql': ['graphql'],
    'machine learning': ['machine learning', 'ml', 'deep learning'],
    'ai': ['artificial intelligence', 'ai'],
    'data science': ['data science', 'data scientist'],
    'tensorflow': ['tensorflow', 'tf'],
    'pytorch': ['pytorch'],
    'pandas': ['pandas'],
    'numpy': ['numpy'],
}


class SkillMatcher:
    """
    Matches user skills with job requirements
    """
    
    @staticmethod
    def normalize_skill(skill: str) -> str:
        """
        Normalize skill name for matching
        
        Args:
            skill: Raw skill name
        
        Returns:
            Normalized skill name
        """
        skill = skill.lower().strip()
        
        # Try exact alias match
        for canonical, aliases in SKILL_ALIASES.items():
            if skill in aliases:
                return canonical
        
        # If no match, return the skill as-is (normalized)
        return skill
    
    @staticmethod
    def extract_skills_from_text(text: str) -> List[str]:
        """
        Extract potential skills from job description text
        Uses simple regex and keyword matching
        
        Args:
            text: Job description text
        
        Returns:
            List of detected skills
        """
        if not text:
            return []
        
        text_lower = text.lower()
        detected_skills = set()
        
        # Check for all known skills
        for canonical, aliases in SKILL_ALIASES.items():
            for alias in aliases:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(alias) + r'\b'
                if re.search(pattern, text_lower):
                    detected_skills.add(canonical)
        
        return list(detected_skills)
    
    @staticmethod
    def calculate_match_score(user_skills: List[str], job_description: str) -> Tuple[float, List[str], List[str]]:
        """
        Calculate match score between user skills and job description
        
        Args:
            user_skills: List of user's skills
            job_description: Job description text
        
        Returns:
            Tuple of (match_percentage, matched_skills, missing_skills)
        """
        if not user_skills:
            return 0.0, [], []
        
        # Normalize user skills
        normalized_user_skills = [SkillMatcher.normalize_skill(s) for s in user_skills]
        normalized_user_skills = list(set(normalized_user_skills))  # Remove duplicates
        
        # Extract skills from job description
        job_skills = SkillMatcher.extract_skills_from_text(job_description)
        
        if not job_skills:
            # If no skills detected in job, do basic text matching
            matched = []
            for skill in normalized_user_skills:
                if skill in job_description.lower():
                    matched.append(skill)
            match_percentage = (len(matched) / len(normalized_user_skills)) * 100
            missing = [s for s in normalized_user_skills if s not in matched]
            return match_percentage, matched, missing
        
        # Calculate intersection
        matched_skills = list(set(normalized_user_skills) & set(job_skills))
        missing_skills = list(set(normalized_user_skills) - set(job_skills))
        
        # Match percentage: matched / total required in job
        match_percentage = (len(matched_skills) / len(job_skills)) * 100
        
        return round(match_percentage, 1), matched_skills, missing_skills
    
    @staticmethod
    def rank_jobs_by_skills(jobs: List[Dict], user_skills: List[str]) -> List[Dict]:
        """
        Rank jobs by skill match percentage
        
        Args:
            jobs: List of job dictionaries
            user_skills: List of user's skills
        
        Returns:
            List of jobs sorted by match score (highest first)
        """
        scored_jobs = []
        
        for job in jobs:
            description = f"{job.get('title', '')} {job.get('description', '')}"
            match_score, matched, missing = SkillMatcher.calculate_match_score(user_skills, description)
            
            # Add match info to job
            job_with_score = job.copy()
            job_with_score['match_score'] = match_score
            job_with_score['matched_skills'] = matched
            job_with_score['missing_skills'] = missing
            
            scored_jobs.append(job_with_score)
        
        # Sort by match score (descending) and then by trust score (descending)
        sorted_jobs = sorted(
            scored_jobs,
            key=lambda x: (x.get('match_score', 0), x.get('trust_score', 0)),
            reverse=True
        )
        
        return sorted_jobs


class RecommendationEngine:
    """
    Generate job recommendations based on skills and preferences
    """
    
    @staticmethod
    def get_recommendations(user_skills: List[str], all_jobs: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        Get top N job recommendations for a user
        
        Args:
            user_skills: User's skills
            all_jobs: All available jobs
            top_n: Number of recommendations
        
        Returns:
            List of top recommended jobs with scores
        """
        # Rank jobs by skill match
        ranked_jobs = SkillMatcher.rank_jobs_by_skills(all_jobs, user_skills)
        
        # Filter jobs with at least some match (optional)
        # recommended = [j for j in ranked_jobs if j['match_score'] > 0]
        
        # Return top N
        return ranked_jobs[:top_n]
