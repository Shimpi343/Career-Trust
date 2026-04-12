from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Opportunity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@recommendations_bp.route('', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get personalized recommendations for user based on skills and interests"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get all opportunities
        opportunities = Opportunity.query.all()
        
        if not opportunities:
            return jsonify({
                'recommendations': [],
                'message': 'No opportunities available yet',
                'user_skills': user.skills or [],
                'user_interests': user.interests or []
            }), 200
        
        # If user has no skills/interests, return all opportunities with equal score
        if not user.skills and not user.interests:
            return jsonify({
                'message': 'Please add your skills and interests for personalized recommendations',
                'recommendations': [
                    {
                        'id': opp.id,
                        'title': opp.title,
                        'company': opp.company,
                        'job_type': opp.job_type,
                        'location': opp.location,
                        'salary': opp.salary,
                        'trust_score': opp.trust_score,
                        'match_score': 50,
                        'description': opp.description[:100] + '...' if len(opp.description) > 100 else opp.description
                    }
                    for opp in opportunities[:5]
                ]
            }), 200
        
        # Build user profile
        user_profile = ' '.join((user.skills or []) + (user.interests or []))
        
        # Build opportunity profiles
        opportunity_profiles = [
            f"{opp.title} {opp.description} {opp.job_type} {opp.requirements or ''}"
            for opp in opportunities
        ]
        
        # Use TF-IDF to vectorize profiles
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        all_profiles = [user_profile] + opportunity_profiles
        
        try:
            tfidf_matrix = vectorizer.fit_transform(all_profiles)
            user_vector = tfidf_matrix[0]
            opportunity_vectors = tfidf_matrix[1:]
            
            # Calculate similarity scores
            similarities = cosine_similarity(user_vector.reshape(1, -1), opportunity_vectors)[0]
        except:
            # Fallback: simple keyword matching
            similarities = []
            user_keywords = set((user.skills or []) + (user.interests or []))
            for opp in opportunities:
                opp_keywords = set((opp.requirements or '').lower().split() + [opp.job_type])
                match = len(user_keywords & opp_keywords) / max(len(user_keywords | opp_keywords), 1)
                similarities.append(match * 100)
            similarities = np.array(similarities)
        
        # Create recommendations with scores
        recommendations = []
        for i, opp in enumerate(opportunities):
            match_score = float(similarities[i]) * 100
            recommendations.append({
                'id': opp.id,
                'title': opp.title,
                'company': opp.company,
                'job_type': opp.job_type,
                'location': opp.location,
                'salary': opp.salary,
                'trust_score': opp.trust_score,
                'match_score': round(match_score, 1),
                'description': opp.description[:100] + '...' if len(opp.description) > 100 else opp.description,
                'source': opp.source
            })
        
        # Sort by match score (descending)
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'recommendations': recommendations[:10],
            'total': len(recommendations),
            'user_skills': user.skills or [],
            'user_interests': user.interests or []
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_job_for_user():
    """Analyze a specific job posting for relevance to user"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        opportunity_id = data.get('opportunity_id')
        
        if not opportunity_id:
            return jsonify({'error': 'opportunity_id required'}), 400
        
        opportunity = Opportunity.query.get(opportunity_id)
        
        if not opportunity:
            return jsonify({'error': 'Opportunity not found'}), 404
        
        # Simple matching logic
        user_keywords = set((user.skills or []) + (user.interests or []))
        opp_text = f"{opportunity.title} {opportunity.description} {opportunity.requirements or ''}".lower()
        
        matches = sum(1 for keyword in user_keywords if keyword.lower() in opp_text)
        match_percentage = (matches / max(len(user_keywords), 1)) * 100 if user_keywords else 50
        
        return jsonify({
            'opportunity_id': opportunity_id,
            'title': opportunity.title,
            'match_score': round(match_percentage, 1),
            'matched_keywords': [k for k in user_keywords if k.lower() in opp_text],
            'recommendation': 'Good match' if match_percentage >= 60 else 'Moderate match' if match_percentage >= 40 else 'Low match'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
