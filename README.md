# CareerTrust: AI-Powered Opportunity Aggregator and Scam Detection System

## Overview

CareerTrust is a comprehensive platform that helps students and early-career professionals discover legitimate career opportunities while protecting them from fraudulent job postings and scam emails. The system combines opportunity aggregation with AI-powered scam detection.

### Key Features

1. **Opportunity Aggregation**: Aggregates career opportunities (internships, hackathons, entry-level jobs) from multiple online platforms
2. **Personalized Recommendations**: Uses NLP and ML algorithms to recommend opportunities based on user skills and interests
3. **Scam Detection**: Analyzes job descriptions and emails to identify suspicious patterns and assign Trust Scores
4. **User-Friendly Interface**: Web application for easy discovery and verification of opportunities

## Project Structure

```
CareerTrust/
├── backend/                 # Flask/FastAPI backend
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── __init__.py
│   ├── requirements.txt    # Python dependencies
│   └── config.py           # Configuration settings
├── frontend/               # React/Vue.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── App.js
│   │   └── index.js
│   ├── public/            # Static files
│   └── package.json
├── ml_models/             # Machine Learning models
│   ├── recommendation_engine/  # NLP-based recommendations
│   ├── scam_detection/         # Fraud detection models
│   └── requirements.txt
├── database/              # Database schemas and migrations
├── tests/                 # Test files
└── docs/                  # Documentation

```

## Tech Stack

### Backend
- **Framework**: Flask or FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT

### Frontend
- **Framework**: React.js
- **Styling**: Tailwind CSS
- **State Management**: Redux or Context API
- **HTTP Client**: Axios

### Machine Learning
- **NLP**: spaCy, NLTK, or Hugging Face Transformers
- **Classification**: Scikit-learn, XGBoost, or PyTorch
- **Vectorization**: TF-IDF or Word2Vec

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## API Endpoints (Planned)

- `GET /api/opportunities` - List opportunities
- `POST /api/opportunities` - Create opportunity
- `GET /api/opportunities/:id` - Get opportunity details
- `POST /api/recommendations` - Get personalized recommendations
- `POST /api/scam-detection/analyze` - Analyze job posting for scams
- `POST /api/users/register` - User registration
- `POST /api/users/login` - User login

## Database Schema (Planned)

- `users` - User profiles and preferences
- `opportunities` - Job postings and internships
- `opportunities_source` - Source platform information
- `user_applications` - User application history
- `scam_reports` - Flagged suspicious postings

## Getting Started

1. Clone the repository
2. Follow Backend Setup instructions
3. Follow Frontend Setup instructions
4. Configure database connection in `config.py`
5. Run migrations
6. Start both backend and frontend servers

## Contributing

Guidelines for contributing to CareerTrust.

## License

MIT License

## Contact & Support

For issues and questions, please open an issue on GitHub.
