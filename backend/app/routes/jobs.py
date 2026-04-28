"""
Job Integration Routes
Endpoints for fetching jobs from external sources and managing them
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Opportunity, User
from app.services import JobAggregator, JobIntegrationError, SkillMatcher, RecommendationEngine
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')


@jobs_bp.route('/fetch', methods=['POST'])
@jwt_required()
def fetch_jobs():
    """
    Fetch jobs from all integrated sources
    Requires authentication (admin check optional for future)
    
    Request body:
    {
        "search_term": "python developer",
        "limit_per_source": 10,
        "auto_add": false
    }
    
    Returns:
    {
        "success": true,
        "sources": {
            "github_jobs": [...],
            "indeed": [...],
            "linkedin": [...]
        },
        "total_jobs": 25,
        "added_to_db": 0
    }
    """
    try:
        data = request.get_json() or {}
        search_term = data.get('search_term', '')
        limit_per_source = min(int(data.get('limit_per_source', 10)), 50)
        auto_add = data.get('auto_add', False)
        
        # Fetch from all sources
        aggregated = JobAggregator.fetch_all_jobs(
            search_term=search_term,
            limit_per_source=limit_per_source
        )
        
        # Count jobs per source
        source_counts = {source: len(jobs) for source, jobs in aggregated.items()}
        total_jobs = sum(source_counts.values())

        if total_jobs == 0:
            aggregated = {
                'demo': JobAggregator.DEMO_JOBS[:limit_per_source]
            }
            source_counts = {source: len(jobs) for source, jobs in aggregated.items()}
            total_jobs = sum(source_counts.values())
        
        # Optionally add to database
        added_count = 0
        if auto_add:
            added_count = _add_jobs_to_db(aggregated)
        
        return jsonify({
            'success': True,
            'sources': source_counts,
            'total_jobs': total_jobs,
            'aggregated': aggregated,
            'added_to_db': added_count
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching jobs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jobs_bp.route('/fetch/<source>', methods=['POST'])
@jwt_required()
def fetch_jobs_from_source(source):
    """
    Fetch jobs from a specific source
    
    Available sources: remoteok, indeed, linkedin, demo
    
    Request body:
    {
        "search_term": "python",
        "location": "USA",
        "limit": 10
    }
    """
    try:
        data = request.get_json() or {}
        search_term = data.get('search_term', '')
        location = data.get('location', 'USA')
        limit = min(int(data.get('limit', 10)), 50)
        
        from app.services import (
            GitHubJobsIntegration,
            DeveloperJobsIntegration,
            JustJoinITIntegration,
            StackOverflowJobsIntegration,
            IndeedIntegration,
            LinkedInIntegration,
            AdzunaIntegration,
            JoobleIntegration,
            JobAggregator,
        )
        
        jobs = []
        
        if source == 'remoteok' or source == 'github_jobs':
            jobs = GitHubJobsIntegration.fetch_jobs(search_term=search_term)[:limit]
        elif source == 'adzuna':
            jobs = AdzunaIntegration.fetch_jobs(search_term=search_term, limit=limit)
        elif source == 'jooble':
            jobs = JoobleIntegration.fetch_jobs(search_term=search_term, limit=limit)
        elif source == 'devto':
            jobs = DeveloperJobsIntegration.fetch_jobs(search_term=search_term, limit=limit)
        elif source == 'justjoinit':
            jobs = JustJoinITIntegration.fetch_jobs(search_term=search_term, limit=limit)
        elif source == 'stackoverflow':
            jobs = StackOverflowJobsIntegration.fetch_jobs(search_term=search_term, limit=limit)
        elif source == 'indeed':
            jobs = IndeedIntegration.fetch_jobs(search_term=search_term, location=location, limit=limit)
        elif source == 'linkedin':
            jobs = LinkedInIntegration.fetch_jobs(search_term=search_term, location=location)[:limit]
        elif source == 'demo':
            jobs = JobAggregator.DEMO_JOBS[:limit]
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown source: {source}. Available: adzuna, jooble, remoteok, devto, justjoinit, stackoverflow, indeed, linkedin, demo'
            }), 400

        if not jobs and source != 'demo':
            jobs = JobAggregator.DEMO_JOBS[:limit]
        
        return jsonify({
            'success': True,
            'source': source,
            'count': len(jobs),
            'jobs': jobs
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching from {source}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jobs_bp.route('/preview', methods=['POST'])
@jwt_required()
def preview_job_import():
    """
    Preview jobs before adding to database
    This doesn't add them yet, just shows what would be added
    
    Request body:
    {
        "jobs": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "description": "...",
                "job_url": "...",
                "source": "GitHub Jobs",
                ...
            }
        ]
    }
    """
    try:
        data = request.get_json() or {}
        jobs = data.get('jobs', [])
        
        if not jobs:
            return jsonify({
                'success': False,
                'error': 'No jobs provided'
            }), 400
        
        # Validate job structure
        preview = []
        errors = []
        
        for i, job in enumerate(jobs):
            if not job.get('title') or not job.get('company'):
                errors.append(f"Job {i}: Missing title or company")
                continue
            
            preview.append({
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'location': job.get('location', 'Not specified'),
                'source': job.get('source', 'Unknown'),
                'job_type': job.get('job_type', 'Job'),
                'trust_score': job.get('trust_score', 50),
            })
        
        return jsonify({
            'success': True,
            'valid_count': len(preview),
            'error_count': len(errors),
            'preview': preview,
            'errors': errors
        }), 200
    
    except Exception as e:
        logger.error(f"Error previewing jobs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jobs_bp.route('/import', methods=['POST'])
@jwt_required()
def import_jobs_to_db():
    """
    Import jobs into the database
    
    Request body:
    {
        "jobs": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "description": "...",
                "job_url": "...",
                "source": "GitHub Jobs",
                "job_type": "Job",
                "trust_score": 90,
                "salary": null,
                "location": "San Francisco"
            }
        ],
        "deduplicate": true
    }
    """
    try:
        data = request.get_json() or {}
        jobs = data.get('jobs', [])
        deduplicate = data.get('deduplicate', True)
        
        if not jobs:
            return jsonify({
                'success': False,
                'error': 'No jobs provided'
            }), 400
        
        added_count = 0
        duplicate_count = 0
        error_count = 0
        
        for job_data in jobs:
            try:
                # Check for duplicates if enabled
                if deduplicate:
                    existing = Opportunity.query.filter_by(
                        title=job_data.get('title'),
                        company=job_data.get('company')
                    ).first()
                    
                    if existing:
                        duplicate_count += 1
                        continue
                
                # Create new opportunity
                posted_at_str = job_data.get('posted_at')
                posted_at = None
                if posted_at_str:
                    try:
                        posted_at = datetime.fromisoformat(posted_at_str)
                    except (ValueError, TypeError):
                        posted_at = None
                
                opportunity = Opportunity(
                    title=job_data.get('title', ''),
                    company=job_data.get('company', ''),
                    description=job_data.get('description', ''),
                    location=job_data.get('location', ''),
                    job_type=job_data.get('job_type', 'Job'),
                    salary=job_data.get('salary'),
                    url=job_data.get('job_url', '') or job_data.get('url', ''),
                    source=job_data.get('source', 'Unknown'),
                    trust_score=job_data.get('trust_score', 50),
                    posted_at=posted_at,
                )
                
                db.session.add(opportunity)
                added_count += 1
            
            except Exception as e:
                logger.error(f"Error adding job {job_data.get('title')}: {str(e)}")
                error_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'added': added_count,
            'duplicates': duplicate_count,
            'errors': error_count,
            'total_processed': len(jobs)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error importing jobs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jobs_bp.route('/sources', methods=['GET'])
def get_available_sources():
    """
    Get list of available job sources and their status
    """
    import os
    
    sources = {
        'adzuna': {
            'name': 'Adzuna',
            'status': 'available' if os.environ.get('ADZUNA_APP_ID') else 'requires_config',
            'requires_auth': True,
            'description': 'Legal job aggregator from 1000+ sources',
            'setup_url': 'https://developer.adzuna.com/'
        },
        'jooble': {
            'name': 'Jooble',
            'status': 'available' if os.environ.get('JOOBLE_API_KEY') else 'requires_config',
            'requires_auth': True,
            'description': 'Job aggregator with good coverage',
            'setup_url': 'https://jooble.org/api/'
        },
        'remoteok': {
            'name': 'RemoteOK',
            'status': 'available',
            'requires_auth': False,
            'description': 'Remote job board with real jobs worldwide'
        },
        'devto': {
            'name': 'Dev.to Jobs',
            'status': 'available',
            'requires_auth': False,
            'description': 'Tech and developer jobs from the Dev.to community'
        },
        'justjoinit': {
            'name': 'JustJoinIT',
            'status': 'available',
            'requires_auth': False,
            'description': 'European tech jobs and startups'
        },
        'stackoverflow': {
            'name': 'Stack Overflow',
            'status': 'available',
            'requires_auth': False,
            'description': 'Verified job listings from Stack Overflow'
        },
        'demo': {
            'name': 'Demo Jobs',
            'status': 'available',
            'requires_auth': False,
            'description': 'Sample jobs for testing'
        }
    }
    
    return jsonify({
        'success': True,
        'sources': sources,
        'message': 'Configure missing sources by setting environment variables'
    }), 200


@jobs_bp.route('/search', methods=['POST'])
@jwt_required()
def search_jobs_by_skills():
    """
    Smart job search with skill matching
    
    Request body:
    {
        "skills": ["python", "react", "aws"],
        "search_term": "developer (optional)",
        "limit": 20,
        "min_match_score": 50
    }
    
    Returns:
    {
        "success": true,
        "results": [
            {
                "title": "...",
                "company": "...",
                "match_score": 85,
                "matched_skills": ["python", "aws"],
                "missing_skills": ["kubernetes"],
                ...
            }
        ],
        "total": 5
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        skills = data.get('skills', [])
        search_term = data.get('search_term', 'developer')
        limit = min(int(data.get('limit', 20)), 100)
        min_match_score = float(data.get('min_match_score', 0))
        
        if not skills:
            return jsonify({
                'success': False,
                'error': 'Please provide at least one skill'
            }), 400
        
        # Fetch jobs from all sources
        aggregated = JobAggregator.fetch_all_jobs(
            search_term=search_term,
            limit_per_source=10
        )
        
        # Flatten jobs
        all_jobs = JobAggregator.flatten_jobs(aggregated)
        
        # Rank by skill match
        ranked_jobs = SkillMatcher.rank_jobs_by_skills(all_jobs, skills)
        
        # Filter by minimum match score if needed
        if min_match_score > 0:
            ranked_jobs = [j for j in ranked_jobs if j.get('match_score', 0) >= min_match_score]
        
        # Limit results
        results = ranked_jobs[:limit]
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'user_skills': skills,
            'search_term': search_term
        }), 200
    
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@jobs_bp.route('/recommendations', methods=['POST'])
@jwt_required()
def get_job_recommendations():
    """
    Get personalized job recommendations based on user skills
    
    Request body:
    {
        "skills": ["python", "django", "postgresql"],
        "top_n": 10
    }
    
    Returns:
    {
        "success": true,
        "recommendations": [
            {
                "title": "Senior Python Developer",
                "company": "...",
                "match_score": 90,
                "matched_skills": [...],
                "missing_skills": [...]
            }
        ]
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        skills = data.get('skills', [])
        top_n = min(int(data.get('top_n', 10)), 50)
        
        if not skills:
            return jsonify({
                'success': False,
                'error': 'Please provide your skills'
            }), 400
        
        # Get all jobs from database (already fetched/stored)
        all_jobs_db = Opportunity.query.limit(100).all()
        if not all_jobs_db:
            recommendations = [
                {**job, 'id': idx}
                for idx, job in enumerate(JobAggregator.DEMO_JOBS[:top_n], start=1)
            ]
            return jsonify({
                'success': True,
                'recommendations': recommendations,
                'total': len(recommendations)
            }), 200

        all_jobs = [
            {
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'description': job.description,
                'location': job.location,
                'salary': job.salary,
                'url': job.url,
                'source': job.source,
                'trust_score': job.trust_score or 70,
                'job_type': job.job_type
            }
            for job in all_jobs_db
        ]
        
        # Get recommendations
        recommendations = RecommendationEngine.get_recommendations(
            skills, all_jobs, top_n
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total': len(recommendations)
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _add_jobs_to_db(aggregated_jobs):
    """
    Helper function to add jobs to database
    """
    added_count = 0
    
    for source, jobs in aggregated_jobs.items():
        for job_data in jobs:
            try:
                # Check for duplicates
                existing = Opportunity.query.filter_by(
                    title=job_data.get('title'),
                    company=job_data.get('company')
                ).first()
                
                if existing:
                    continue
                
                # Create opportunity
                opportunity = Opportunity(
                    title=job_data.get('title', ''),
                    company=job_data.get('company', ''),
                    description=job_data.get('description', ''),
                    location=job_data.get('location', ''),
                    job_type=job_data.get('job_type', 'Job'),
                    salary=job_data.get('salary'),
                    url=job_data.get('job_url', '') or job_data.get('url', ''),
                    source=job_data.get('source', 'Unknown'),
                    trust_score=job_data.get('trust_score', 50),
                    posted_at=datetime.fromisoformat(
                        job_data.get('posted_at', datetime.now().isoformat())
                    ) if job_data.get('posted_at') else datetime.now(),
                )
                
                db.session.add(opportunity)
                added_count += 1
            
            except Exception as e:
                logger.error(f"Error adding job: {str(e)}")
                continue
    
    db.session.commit()
    return added_count
