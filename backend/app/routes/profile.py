"""
User Profile Routes
Endpoints for user profiles, resumes, preferences, and job bookmarking
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Opportunity, SavedJob
from app.services import ResumeParser, AdvancedSkillMatcher, ResumeAnalyzer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')


@profile_bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'profile': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'skills': user.skills or [],
                'experience_years': user.experience_years,
                'preferences': user.preferences or {},
                'resume_text': bool(user.resume_text),  # Just indicate if it exists
                'resume_skills': user.resume_skills or [],
                'created_at': user.created_at.isoformat()
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@profile_bp.route('/skills', methods=['POST'])
@jwt_required()
def update_skills():
    """
    Update user skills manually
    
    Request body:
    {
        "skills": ["python", "react", "aws"],
        "experience_years": 5
    }
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        data = request.get_json() or {}
        skills = data.get('skills', [])
        experience_years = data.get('experience_years')
        
        # Normalize and validate skills
        normalized_skills = [s.lower().strip() for s in skills if s]
        normalized_skills = list(set(normalized_skills))  # Remove duplicates
        
        user.skills = normalized_skills
        if experience_years is not None:
            user.experience_years = int(experience_years)
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Skills updated',
            'skills': user.skills,
            'experience_years': user.experience_years
        }), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating skills: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@profile_bp.route('/resume', methods=['POST'])
@jwt_required()
def upload_resume():
    """
    Upload and parse resume
    Supports PDF and DOCX files
    Auto-extracts skills and experience
    
    Multipart form data:
    - file: Resume file (PDF/DOCX)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'pdf', 'docx', 'doc'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {allowed_extensions}'
            }), 400
        
        # Read file content
        file_content = file.read()
        
        # Parse resume
        resume_text, extracted_skills = ResumeParser.parse_resume(file_content, file.filename)
        
        # Analyze resume for additional info
        experience_years = ResumeAnalyzer.extract_experience_level(resume_text)
        education = ResumeAnalyzer.extract_education(resume_text)
        
        # Update user
        user.resume_text = resume_text
        user.resume_skills = list(set(extracted_skills))  # Deduplicate
        user.experience_years = experience_years
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded and parsed',
            'extracted_skills': user.resume_skills,
            'experience_years': experience_years,
            'education_found': education,
            'file_size': len(file_content)
        }), 200
    
    except ValueError as e:
        logger.error(f"Resume parsing error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error uploading resume: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@profile_bp.route('/preferences', methods=['POST'])
@jwt_required()
def set_preferences():
    """
    Set job search preferences
    
    Request body:
    {
        "min_salary": 80000,
        "max_salary": 150000,
        "job_type": ["full-time", "contract"],
        "location": ["remote", "san francisco", "new york"],
        "industries": ["tech", "fintech", "ai"],
        "company_size": ["startup", "scale-up", "enterprise"]
    }
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        data = request.get_json() or {}
        preferences = {
            'min_salary': data.get('min_salary'),
            'max_salary': data.get('max_salary'),
            'job_type': data.get('job_type', []),
            'location': data.get('location', []),
            'industries': data.get('industries', []),
            'company_size': data.get('company_size', []),
        }
        
        user.preferences = preferences
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Preferences updated',
            'preferences': preferences
        }), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating preferences: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@profile_bp.route('/saved-jobs', methods=['GET'])
@jwt_required()
def get_saved_jobs():
    """
    Get user's saved/bookmarked jobs
    """
    try:
        user_id = get_jwt_identity()
        
        saved_jobs = db.session.query(SavedJob, Opportunity).join(
            Opportunity, SavedJob.opportunity_id == Opportunity.id
        ).filter(SavedJob.user_id == user_id).all()
        
        results = []
        for saved, job in saved_jobs:
            results.append({
                'saved_job_id': saved.id,
                'job': {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'salary': job.salary,
                    'url': job.url,
                    'source': job.source,
                    'trust_score': job.trust_score,
                },
                'match_score': saved.match_score,
                'notes': saved.notes,
                'applied': saved.applied,
                'saved_at': saved.saved_at.isoformat(),
                'applied_at': saved.applied_at.isoformat() if saved.applied_at else None
            })
        
        return jsonify({
            'success': True,
            'saved_jobs': results,
            'total': len(results)
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching saved jobs: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@profile_bp.route('/save-job', methods=['POST'])
@jwt_required()
def save_job():
    """
    Save/bookmark a job
    
    Request body:
    {
        "opportunity_id": 123,
        "match_score": 85.5,
        "notes": "Interested in this role"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        opportunity_id = data.get('opportunity_id')
        match_score = data.get('match_score')
        notes = data.get('notes', '')
        
        if not opportunity_id:
            return jsonify({'success': False, 'error': 'opportunity_id required'}), 400
        
        # Check if job exists
        job = Opportunity.query.get(opportunity_id)
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        # Check if already saved
        existing = SavedJob.query.filter_by(
            user_id=user_id,
            opportunity_id=opportunity_id
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'Job already saved',
                'saved_job_id': existing.id
            }), 200  # Not an error, just already there
        
        # Create saved job
        saved_job = SavedJob(
            user_id=user_id,
            opportunity_id=opportunity_id,
            match_score=match_score,
            notes=notes
        )
        
        db.session.add(saved_job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Job saved',
            'saved_job_id': saved_job.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving job: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@profile_bp.route('/unsave-job/<int:saved_job_id>', methods=['DELETE'])
@jwt_required()
def unsave_job(saved_job_id):
    """
    Remove a saved job
    """
    try:
        user_id = get_jwt_identity()
        saved_job = SavedJob.query.filter_by(
            id=saved_job_id,
            user_id=user_id
        ).first()
        
        if not saved_job:
            return jsonify({'success': False, 'error': 'Saved job not found'}), 404
        
        db.session.delete(saved_job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Job removed from saved list'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error removing saved job: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@profile_bp.route('/mark-applied', methods=['POST'])
@jwt_required()
def mark_job_applied():
    """
    Mark a saved job as applied to
    
    Request body:
    {
        "saved_job_id": 5
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        saved_job_id = data.get('saved_job_id')
        
        if not saved_job_id:
            return jsonify({'success': False, 'error': 'saved_job_id required'}), 400
        
        saved_job = SavedJob.query.filter_by(
            id=saved_job_id,
            user_id=user_id
        ).first()
        
        if not saved_job:
            return jsonify({'success': False, 'error': 'Saved job not found'}), 404
        
        saved_job.applied = True
        saved_job.applied_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Job marked as applied',
            'applied_at': saved_job.applied_at.isoformat()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking job applied: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
