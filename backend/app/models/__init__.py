from app import db
from datetime import datetime

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    skills = db.Column(db.JSON)
    interests = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Opportunity(db.Model):
    """Opportunity model"""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    job_type = db.Column(db.String(50), nullable=False)  # internship, job, hackathon
    location = db.Column(db.String(255))
    salary = db.Column(db.String(100))
    requirements = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    posted_at = db.Column(db.DateTime)  # When the job was originally posted
    trust_score = db.Column(db.Float, default=100)
    source = db.Column(db.String(100))  # LinkedIn, Indeed, etc.
    url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Opportunity {self.title}>'

class Application(db.Model):
    """User application history"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    status = db.Column(db.String(50))  # applied, rejected, accepted
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    response_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Application user_id={self.user_id} opportunity_id={self.opportunity_id}>'

class ScamReport(db.Model):
    """Scam detection and flagged postings"""
    __tablename__ = 'scam_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))
    text_content = db.Column(db.Text)
    scam_score = db.Column(db.Float)
    is_flagged = db.Column(db.Boolean, default=False)
    suspicious_keywords = db.Column(db.JSON)
    analysis_result = db.Column(db.JSON)
    reported_by_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ScamReport opportunity_id={self.opportunity_id}>'
