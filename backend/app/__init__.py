import os

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

    frontend_origins = [
        os.getenv('FRONTEND_URL', 'https://careertrust.netlify.app'),
        'http://localhost:3000',
        'http://localhost:5173',
        'http://localhost:5000',
    ]
    CORS(
        app,
        resources={r"/api/*": {"origins": frontend_origins}},
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    )
    
    # Register blueprints
    from app.routes import auth_bp, opportunities_bp, recommendations_bp, scam_detection_bp, jobs_bp, profile_bp, analytics_bp, notifications_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(opportunities_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(scam_detection_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(notifications_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        from app.services.notification_service import start_notification_scheduler
        start_notification_scheduler(app)
    
    return app
