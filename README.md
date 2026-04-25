# CareerTrust

CareerTrust is an AI-powered career platform that helps students and early-career professionals discover verified opportunities, understand fit, and present themselves more effectively.

It combines live job aggregation, skill-based recommendations, resume parsing, saved-job tracking, and trust scoring in a single workflow that is easy to explain in a live presentation.

## What It Does
- Aggregates jobs from multiple sources, including RemoteOK, Dev.to, JustJoinIT, Stack Overflow, Adzuna, and Jooble when configured.
- Scores jobs against a user profile using skill matching and TF-IDF similarity.
- Parses PDF and DOCX resumes to extract skills automatically.
- Tracks saved jobs, applications, and profile completeness.
- Surfaces trust signals so suspicious or low-quality listings are easier to spot.

## Tech Stack
- Backend: Flask, SQLAlchemy, Flask-JWT-Extended, Flask-CORS
- Frontend: React, React Router, Axios, Tailwind CSS
- Data: SQLite for development, PostgreSQL-compatible schema for production
- AI / NLP: scikit-learn, TF-IDF, custom skill matching logic

## Repository Layout
- [backend](backend) - Flask API, models, services, and job integrations
- [frontend](frontend) - React interface for the product demo
- [docs](docs) - Supporting documentation
- [tests](tests) - Endpoint and workflow checks
- [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) - Demo script and talking points

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Demo Flow
1. Open the home page and explain the product value.
2. Create a profile and add skills or upload a resume.
3. Open Recommendations to show match scores and missing skills.
4. Open Job Integration to fetch live jobs and import them.
5. Open Opportunities and Dashboard to show the finished workflow.

## Demo Account
- Email: `student1@example.com`
- Password: `password123`

## Key API Areas
- Authentication: `/api/auth/login`, `/api/auth/register`
- Profile: `/api/profile/me`, `/api/profile/skills`, `/api/profile/preferences`
- Jobs: `/api/jobs/fetch`, `/api/jobs/fetch/<source>`, `/api/jobs/import`, `/api/jobs/recommendations`
- Analytics: `/api/analytics/dashboard`, `/api/analytics/job-market`
- Scam detection: `/api/scam-detection/report`, `/api/scam-detection/<opportunity_id>`

## Presentation Notes
This project is strongest when presented as a real product demo rather than a code showcase. Lead with the problem, show the live workflow, then point out the trust layer and recommendation engine.

For a structured walkthrough, use [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md).
