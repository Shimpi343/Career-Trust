"""WSGI entry point for production (Render, Heroku, etc.)"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app, db

config_name = os.getenv('FLASK_CONFIG')
if not config_name:
    config_name = 'production' if os.getenv('DATABASE_URL') else 'development'

app = create_app(config_name)

# Create database tables on startup
with app.app_context():
    db.create_all()
    print("Database tables initialized!")

if __name__ == "__main__":
    app.run()
