# CareerTrust Development Guide

## Project Overview
CareerTrust is an AI-powered platform that:
1. Aggregates career opportunities from multiple sources
2. Provides personalized recommendations using NLP
3. Detects fraudulent job postings using ML

## Architecture

### Backend (Flask)
- RESTful API for opportunities, recommendations, and scam detection
- JWT authentication
- SQLAlchemy ORM with PostgreSQL

### Frontend (React)
- User-friendly interface for browsing opportunities
- Dashboard for application history
- Trust score visualization

### Machine Learning
- **Recommendation Engine**: TF-IDF vectorization + cosine similarity
- **Scam Detection**: Random Forest classifier with keyword analysis

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Database
```bash
# Install PostgreSQL and create database
createdb careertrust_dev

# Apply schema
psql careertrust_dev < database/schema.sql
```

## API Documentation

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Opportunities
- `GET /api/opportunities` - List all opportunities
- `GET /api/opportunities/:id` - Get opportunity details
- `POST /api/opportunities` - Create opportunity (admin)

### Recommendations
- `GET /api/recommendations` - Get personalized recommendations

### Scam Detection
- `POST /api/scam-detection/analyze` - Analyze job posting

## Contributing
1. Create a feature branch
2. Make changes
3. Write tests
4. Submit pull request

## Key Files
- `backend/config.py` - Configuration settings
- `backend/app/__init__.py` - Flask app factory
- `frontend/src/api.js` - API client
- `ml_models/` - ML model implementation

## Next Steps
1. Set up PostgreSQL database
2. Implement data sources for opportunity aggregation
3. Train ML models with sample data
4. Add email parsing for scam detection
5. Implement user profile management
