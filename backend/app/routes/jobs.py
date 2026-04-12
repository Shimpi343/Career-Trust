"""
Job Integration Routes
Endpoints for fetching jobs from external sources and managing them
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Opportunity, User
from app.services import JobAggregator, JobIntegrationError
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
        
        from app.services import GitHubJobsIntegration, DeveloperJobsIntegration, JustJoinITIntegration, StackOverflowJobsIntegration, IndeedIntegration, LinkedInIntegration, JobAggregator
        
        jobs = []
        
        if source == 'remoteok' or source == 'github_jobs':
            jobs = GitHubJobsIntegration.fetch_jobs(search_term=search_term)[:limit]
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
                'error': f'Unknown source: {source}. Available: remoteok, devto, justjoinit, stackoverflow, indeed, linkedin, demo'
            }), 400
        
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
        'indeed': {
            'name': 'Indeed',
            'status': 'available' if os.environ.get('INDEED_API_KEY') else 'requires_config',
            'requires_auth': True,
            'description': 'Large job board (requires API key)',
            'setup_url': 'https://opensource.indeedeng.io/api-documentation/'
        },
        'linkedin': {
            'name': 'LinkedIn',
            'status': 'requires_config',
            'requires_auth': True,
            'description': 'Professional network (requires email/password)',
            'note': 'Install with: pip install linkedin-api'
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
