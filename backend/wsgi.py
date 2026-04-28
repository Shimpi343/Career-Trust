"""WSGI entry point for production (Render, Heroku, etc.)"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app, db

app = create_app()

# Create database tables on startup
with app.app_context():
    db.create_all()
    print("Database tables initialized!")

if __name__ == "__main__":
    app.run()
