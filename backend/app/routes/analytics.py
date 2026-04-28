"""
Analytics Routes
Endpoints for user analytics, application tracking, and job market insights
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Opportunity, SavedJob, Application
from app.services import SkillMatcher
from datetime import datetime, timedelta
from sqlalchemy import func
from collections import Counter
import logging

logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_analytics_dashboard():
    """
    Get user's analytics dashboard
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Count saved jobs
        saved_count = SavedJob.query.filter_by(user_id=user_id).count()
        applied_count = SavedJob.query.filter_by(user_id=user_id, applied=True).count()
        
        # Count applications
        app_count = Application.query.filter_by(user_id=user_id).count()
        
        # Get stats from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_saves = SavedJob.query.filter(
            SavedJob.user_id == user_id,
            SavedJob.saved_at >= thirty_days_ago
        ).count()
        
        # Calculate average match score
        saved_jobs = SavedJob.query.filter_by(user_id=user_id).all()
        avg_match = 0
        if saved_jobs:
            match_scores = [j.match_score for j in saved_jobs if j.match_score]
            if match_scores:
                avg_match = sum(match_scores) / len(match_scores)
        
        return jsonify({
            'success': True,
            'dashboard': {
                'total_saved_jobs': saved_count,
                'jobs_applied_to': applied_count,
                'total_applications': app_count,
                'recent_saves_30d': recent_saves,
                'average_match_score': round(avg_match, 1),
                'user_skills': user.skills or [],
                'profile_completion': _calculate_profile_completion(user),
                'missing_sections': _get_missing_profile_sections(user)
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@analytics_bp.route('/job-market', methods=['GET'])
@jwt_required()
def get_job_market_insights():
    """
    Get insights about the job market
    Top skills, companies hiring, locations, etc.
    """
    try:
        # Get all opportunities
        all_jobs = Opportunity.query.limit(1000).all()
        
        if not all_jobs:
            return jsonify({
                'success': True,
                'insights': {
                    'total_jobs': 0,
                    'top_skills': [],
                    'top_companies': [],
                    'top_locations': [],
                    'average_trust_score': 0
                }
            }), 200
        
        # Count by company
        company_counts = db.session.query(
            Opportunity.company,
            func.count(Opportunity.id).label('count')
        ).group_by(Opportunity.company).order_by(func.count(Opportunity.id).desc()).limit(10).all()
        
        # Count by location
        location_counts = db.session.query(
            Opportunity.location,
            func.count(Opportunity.id).label('count')
        ).group_by(Opportunity.location).order_by(func.count(Opportunity.id).desc()).limit(10).all()
        
        # Count by source
        source_counts = db.session.query(
            Opportunity.source,
            func.count(Opportunity.id).label('count')
        ).group_by(Opportunity.source).order_by(func.count(Opportunity.id).desc()).all()
        
        # Average trust score
        avg_trust = db.session.query(func.avg(Opportunity.trust_score)).scalar() or 0
        
        # Extract and count top skills from job descriptions
        skill_counter = Counter()
        for job in all_jobs:
            if job.description:
                skills = SkillMatcher.extract_skills_from_text(job.description)
                skill_counter.update(skills)
        
        top_skills = skill_counter.most_common(15)
        
        return jsonify({
            'success': True,
            'insights': {
                'total_jobs': len(all_jobs),
                'job_types': dict(db.session.query(
                    Opportunity.job_type,
                    func.count(Opportunity.id)
                ).group_by(Opportunity.job_type).all() or []),
                'top_companies': [
                    {'company': c[0], 'count': c[1]} for c in company_counts
                ],
                'top_locations': [
                    {'location': l[0], 'count': l[1]} for l in location_counts
                ],
                'sources': [
                    {'source': s[0], 'count': s[1]} for s in source_counts
                ],
                'top_skills': [
                    {'skill': skill, 'count': count} for skill, count in top_skills
                ],
                'average_trust_score': round(float(avg_trust), 1)
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching market insights: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@analytics_bp.route('/application-history', methods=['GET'])
@jwt_required()
def get_application_history():
    """
    Get user's application history
    """
    try:
        user_id = get_jwt_identity()
        
        # Get all saved jobs with applied status
        saved_jobs = db.session.query(SavedJob, Opportunity).join(
            Opportunity, SavedJob.opportunity_id == Opportunity.id
        ).filter(SavedJob.user_id == user_id).order_by(SavedJob.saved_at.desc()).all()
        
        applied_jobs = []
        for saved, job in saved_jobs:
            if saved.applied:
                applied_jobs.append({
                    'job': {
                        'id': job.id,
                        'title': job.title,
                        'company': job.company,
                        'location': job.location,
                        'salary': job.salary,
                        'source': job.source,
                    },
                    'match_score': saved.match_score,
                    'applied_date': saved.applied_at.isoformat() if saved.applied_at else None,
                    'notes': saved.notes
                })
        
        # Group by month
        history_by_month = {}
        for item in applied_jobs:
            if item['applied_date']:
                month_key = item['applied_date'][:7]  # YYYY-MM
                if month_key not in history_by_month:
                    history_by_month[month_key] = []
                history_by_month[month_key].append(item)
        
        return jsonify({
            'success': True,
            'total_applications': len(applied_jobs),
            'applications': applied_jobs,
            'by_month': history_by_month
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching application history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@analytics_bp.route('/skills-analysis', methods=['POST'])
@jwt_required()
def analyze_skills():
    """
    Analyze user's skills and market demand
    
    Request body:
    {
        "skills": ["python", "react", "aws"]
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        skills = data.get('skills', [])
        
        if not skills:
            return jsonify({'success': False, 'error': 'No skills provided'}), 400
        
        # Get all jobs
        all_jobs = Opportunity.query.limit(5000).all()
        
        # Analyze each skill
        from app.services import SkillMatcher
        
        skill_analysis = {}
        for skill in skills:
            job_count = 0
            avg_match = 0
            salaries = []
            
            match_scores = []
            for job in all_jobs:
                description = f"{job.title} {job.description}"
                score, _, _ = SkillMatcher.calculate_match_score([skill], description)
                
                if score > 0:
                    job_count += 1
                    match_scores.append(score)
                    if job.salary:
                        try:
                            # Try to extract first salary number
                            import re
                            salary_nums = re.findall(r'\d+,?\d*', job.salary)
                            if salary_nums:
                                salaries.append(int(salary_nums[0].replace(',', '')))
                        except:
                            pass
            
            avg_match = sum(match_scores) / len(match_scores) if match_scores else 0
            avg_salary = sum(salaries) / len(salaries) if salaries else None
            
            skill_analysis[skill] = {
                'job_postings': job_count,
                'average_match_score': round(avg_match, 1),
                'estimated_salary': avg_salary,
                'demand_level': _classify_demand(job_count, len(all_jobs))
            }
        
        return jsonify({
            'success': True,
            'skill_analysis': skill_analysis
        }), 200
    
    except Exception as e:
        logger.error(f"Error analyzing skills: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


def _calculate_profile_completion(user) -> int:
    """
    Calculate profile completion percentage
    """
    completion = 0
    total_fields = 6
    
    if user.email:
        completion += 1
    if user.username:
        completion += 1
    if user.skills and len(user.skills) > 0:
        completion += 1
    if user.experience_years and user.experience_years > 0:
        completion += 1
    if user.resume_text:
        completion += 1
    if user.preferences and len(user.preferences) > 0:
        completion += 1
    
    return int((completion / total_fields) * 100)


def _get_missing_profile_sections(user) -> list:
    """
    Return a friendly list of profile sections that still need attention.
    """
    missing = []

    if not user.skills:
        missing.append('Add skills')
    if not user.experience_years:
        missing.append('Add experience')
    if not user.resume_text:
        missing.append('Upload resume')
    if not user.preferences or not len(user.preferences):
        missing.append('Set preferences')

    return missing


def _classify_demand(job_count: int, total_jobs: int) -> str:
    """
    Classify skill demand level
    """
    if total_jobs == 0:
        return "unknown"
    
    percentage = (job_count / total_jobs) * 100
    
    if percentage > 10:
        return "very_high"
    elif percentage > 5:
        return "high"
    elif percentage > 1:
        return "medium"
    else:
        return "low"
