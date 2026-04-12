from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Opportunity

opportunities_bp = Blueprint('opportunities', __name__, url_prefix='/api/opportunities')

@opportunities_bp.route('', methods=['GET'])
def get_opportunities():
    """Get all opportunities with filtering and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        job_type = request.args.get('type')
        
        query = Opportunity.query
        
        if job_type:
            query = query.filter_by(job_type=job_type)
        
        opportunities = query.paginate(page=page, per_page=per_page)
        
        result = {
            'total': opportunities.total,
            'pages': opportunities.pages,
            'current_page': page,
            'opportunities': [
                {
                    'id': opp.id,
                    'title': opp.title,
                    'company': opp.company,
                    'description': opp.description,
                    'job_type': opp.job_type,
                    'location': opp.location,
                    'salary': opp.salary,
                    'trust_score': opp.trust_score,
                    'source': opp.source
                }
                for opp in opportunities.items
            ]
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@opportunities_bp.route('/<int:opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    """Get specific opportunity by ID"""
    try:
        opportunity = Opportunity.query.get(opportunity_id)
        
        if not opportunity:
            return jsonify({'error': 'Opportunity not found'}), 404
        
        return jsonify({
            'id': opportunity.id,
            'title': opportunity.title,
            'company': opportunity.company,
            'description': opportunity.description,
            'job_type': opportunity.job_type,
            'location': opportunity.location,
            'salary': opportunity.salary,
            'requirements': opportunity.requirements,
            'deadline': opportunity.deadline,
            'trust_score': opportunity.trust_score,
            'source': opportunity.source,
            'url': opportunity.url
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@opportunities_bp.route('', methods=['POST'])
@jwt_required()
def create_opportunity():
    """Create new opportunity (admin only)"""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'company', 'description', 'job_type']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        opportunity = Opportunity(
            title=data['title'],
            company=data['company'],
            description=data['description'],
            job_type=data['job_type'],
            location=data.get('location'),
            salary=data.get('salary'),
            requirements=data.get('requirements'),
            deadline=data.get('deadline'),
            source=data.get('source'),
            url=data.get('url'),
            trust_score=100  # Default score, will be updated by scam detection
        )
        
        db.session.add(opportunity)
        db.session.commit()
        
        return jsonify({'message': 'Opportunity created', 'opportunity_id': opportunity.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
