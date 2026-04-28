#!/usr/bin/env python
"""
Setup script to create a test user with email notification preferences enabled.
Run this after starting the Flask server to set up test data.
"""
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

def setup_notification_test_user():
    """Create a test user with email notifications enabled."""
    app = create_app()
    
    TEST_PASSWORD = "password123"
    
    with app.app_context():
        # Check if test user already exists
        test_user = User.query.filter_by(email='test@careertrust.local').first()
        
        if test_user:
            print(f"Test user already exists (ID: {test_user.id})")
            print(f"Email: {test_user.email}")
            # Update password to ensure it's correct
            print(f"Updating password to: {TEST_PASSWORD}")
            test_user.password_hash = generate_password_hash(TEST_PASSWORD)
        else:
            # Create new test user with hashed password
            test_user = User(
                username='testuser',
                email='test@careertrust.local',
                password_hash=generate_password_hash(TEST_PASSWORD)
            )
            db.session.add(test_user)
            db.session.commit()
            print(f"Created new test user (ID: {test_user.id})")
            print(f"Email: {test_user.email}")
        
        # Update notification preferences
        preferences = test_user.preferences or {}
        preferences['notifications'] = {
            'email_alerts': True,           # Enable email alerts
            'digest_frequency': 'daily',     # daily or weekly
            'digest_day': 'monday',         # For weekly digests
            'digest_time': '08:00',         # UTC time for daily/weekly digest
            'email': test_user.email,       # Email to send notifications to
            'last_alert_sent_at': None,
            'last_digest_sent_at': None,
        }
        
        # Also set user profile data for better recommendations
        test_user.skills = ['Python', 'JavaScript', 'React', 'SQL', 'Machine Learning']
        test_user.interests = ['Backend Development', 'AI', 'Data Science', 'Full Stack']
        test_user.experience_years = 3
        test_user.preferences = preferences
        test_user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        print("\n✅ Notification preferences enabled:")
        print(f"   - Email Alerts: {preferences['notifications']['email_alerts']}")
        print(f"   - Digest Frequency: {preferences['notifications']['digest_frequency']}")
        print(f"   - Email: {preferences['notifications']['email']}")
        print(f"   - Skills: {', '.join(test_user.skills)}")
        print(f"   - Interests: {', '.join(test_user.interests)}")
        
        print(f"\n📋 Test user ready:")
        print(f"   - User ID: {test_user.id}")
        print(f"   - Email: {test_user.email}")
        print(f"   - Username: {test_user.username}")
        print(f"   - Password: {TEST_PASSWORD}")
        
        print(f"\n🔐 Get JWT token by logging in:")
        print(f"   POST http://localhost:5000/api/auth/login")
        print(f"   Body: {{'email': 'test@careertrust.local', 'password': '{TEST_PASSWORD}'}}")
        
        print(f"\n📧 Test notification endpoints:")
        print(f"   GET  /api/notifications/settings (get current settings)")
        print(f"   POST /api/notifications/settings (update settings)")
        print(f"   POST /api/notifications/test-email (send test email)")
        print(f"   POST /api/notifications/digest (manually trigger digest)")
        
        print(f"\n📅 Scheduler jobs (running in background):")
        print(f"   - Hourly: Check for new job matches and send alerts")
        print(f"   - Daily: Send daily digest at 08:00 UTC")
        print(f"   - Weekly: Send weekly digest every Monday at 08:30 UTC")

if __name__ == '__main__':
    setup_notification_test_user()
