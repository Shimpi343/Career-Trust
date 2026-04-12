from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth_bp, opportunities_bp, recommendations_bp, scam_detection_bp, jobs_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(opportunities_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(scam_detection_bp)
    app.register_blueprint(jobs_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
