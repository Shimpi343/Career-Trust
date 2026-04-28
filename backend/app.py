from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
