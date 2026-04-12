# CareerTrust - Architecture & Code Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React - TODO)                  │
│  Dashboard │ Profile │ Search │ Bookmarks │ Analytics       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         │ (axios)
┌────────────────────────┴────────────────────────────────────┐
│                  FLASK REST API (BACKEND)                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │  Auth Routes    │  │  Job Routes     │  │  Profile   │  │
│  │  - Register     │  │  - Search       │  │  Routes    │  │
│  │  - Login        │  │  - Recommend    │  │  - Updates │  │
│  └─────────────────┘  │  - Import       │  └────────────┘  │
│                       └─────────────────┘                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │ Analytics Routes│  │ Scam Detection  │  │ SavedJobs  │  │
│  │ - Dashboard     │  │ Routes          │  │ Routes     │  │
│  │ - Market        │  │ - Report        │  │ - Bookmark │  │
│  │ - Skills        │  │ - Check         │  │ - List     │  │
│  └─────────────────┘  └─────────────────┘  └────────────┘  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                      SERVICE LAYER                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  JobAggregator          SkillMatcher      ResumeParser      │
│  ├─ Adzuna API          ├─ Skill Extract  ├─ PDF Extract  │
│  ├─ Jooble API          ├─ Matching       ├─ DOCX Extract │
│  ├─ RemoteOK            └─ Scoring        └─ Skill Parse  │
│  ├─ Dev.to                                                  │
│  ├─ JustJoinIT       AdvancedSkillMatcher                  │
│  └─ Stack Overflow   ├─ TF-IDF            ResumeAnalyzer  │
│                       ├─ NLP Processing    ├─ Experience  │
│  RecommendationSvc    └─ Scoring          └─ Education    │
│  ├─ Vector Match                                           │
│  └─ Ranking          ScamDetectionSvc                      │
│                      ├─ Pattern Match                       │
│                      └─ Trust Scoring                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                           │
                       SQLAlchemy ORM
                           │
┌────────────────────────────┴──────────────────────────────────┐
│              DATABASE (SQLite / PostgreSQL)                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐  ┌───────────────┐  ┌─────────────┐           │
│  │  Users   │  │ Opportunities │  │ SavedJobs   │           │
│  │  Table   │  │     Table      │  │    Table    │           │
│  └──────────┘  └───────────────┘  └─────────────┘           │
│                                                               │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────┐       │
│  │ Applications │  │  ScamReports  │  │ Preferences │       │
│  │    Table     │  │     Table      │  │    (JSON)   │       │
│  └──────────────┘  └───────────────┘  └─────────────┘       │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure & Responsibilities

### **Core Application Files**

```
backend/
│
├── 📄 app.py
│   Purpose: Flask app entry point
│   >>> from app import create_app
│   >>> app = create_app()
│   >>> app.run()
│
├── 📄 config.py
│   Purpose: Configuration management (dev/prod)
│   - Database URI
│   - JWT secret
│   - API keys for job services
│
├── 📄 requirements.txt
│   Purpose: Python dependencies
│   Contains:
│   - Flask==3.0.0
│   - Flask-SQLAlchemy==3.0
│   - Flask-JWT-Extended==4.4.4
│   - PyPDF2==latest
│   - python-docx==latest
│   - nltk==latest
│   - scikit-learn==latest
│   - numpy, pandas
│
└── 📁 app/
    │
    ├── 📄 __init__.py
    │   Purpose: Flask app factory
    │   - Creates Flask app instance
    │   - Initializes database (SQLAlchemy)
    │   - Registers all blueprints (routes)
    │   - Configures JWT
    │   - Sets up error handlers
    │
    ├── 📁 models/
    │   └── 📄 __init__.py
    │       Purpose: Database models using SQLAlchemy ORM
    │       Models:
    │       ├── User (id, username, email, skills[], experience, resume)
    │       ├── Opportunity (id, title, company, location, description)
    │       ├── SavedJob (user_id, opportunity_id, match_score, applied)
    │       ├── Application (user_id, opportunity_id, status)
    │       └── ScamReport (opportunity_id, reporter_id, reason)
    │
    ├── 📁 routes/
    │   │   Purpose: API endpoint handlers (Flask blueprints)
    │   │
    │   ├── 📄 __init__.py
    │   │   - Imports all blueprints
    │   │   - Exposes for app factory registration
    │   │
    │   ├── 📄 auth.py (2 endpoints)
    │   │   POST /api/auth/register  → Create new user
    │   │   POST /api/auth/login     → Get JWT token
    │   │   Dependencies: User model, JWT
    │   │
    │   ├── 📄 jobs.py (3+ endpoints)
    │   │   POST /api/jobs/import              → Bulk add jobs
    │   │   GET  /api/jobs/search              → Search by skills
    │   │   POST /api/jobs/recommendations     → Get matches
    │   │   Dependencies: JobAggregator, SkillMatcher, Opportunity
    │   │
    │   ├── 📄 profile.py (8 endpoints)
    │   │   GET  /api/profile/me               → Get user profile
    │   │   POST /api/profile/skills           → Update skills
    │   │   POST /api/profile/resume           → Upload resume
    │   │   POST /api/profile/preferences      → Set preferences
    │   │   GET  /api/profile/saved-jobs       → List bookmarks
    │   │   POST /api/profile/save-job         → Bookmark job
    │   │   DEL  /api/profile/unsave-job/<id>  → Remove bookmark
    │   │   POST /api/profile/mark-applied     → Mark as applied
    │   │   Dependencies: ResumeParser, AdvancedSkillMatcher, SavedJob
    │   │
    │   ├── 📄 analytics.py (4 endpoints)
    │   │   GET  /api/analytics/dashboard           → User stats
    │   │   GET  /api/analytics/job-market          → Market insights
    │   │   GET  /api/analytics/application-history → Applications
    │   │   POST /api/analytics/skills-analysis     → Skill demand
    │   │   Dependencies: SavedJob, Application, Opportunity
    │   │
    │   ├── 📄 scam_detection.py (2+ endpoints)
    │   │   GET  /api/scam-detection/<id>     → Check if flagged
    │   │   POST /api/scam-detection/report   → Report job
    │   │   Dependencies: ScamDetectionService, ScamReport
    │   │
    │   ├── 📄 recommendations.py
    │   │   GET /api/recommendations → Personalized recommendations
    │   │   Dependencies: RecommendationEngine
    │   │
    │   └── 📄 opportunities.py
    │       CRUD operations for job opportunities
    │       Dependencies: Opportunity model
    │
    ├── 📁 services/
    │   │   Purpose: Business logic layer (reusable service classes)
    │   │
    │   ├── 📄 __init__.py
    │   │   - Exports all service classes:
    │   │     from app.services import ResumeParser, SkillMatcher, etc.
    │   │
    │   ├── 📄 job_integrations.py
    │   │   Class: JobAggregator
    │   │   Methods:
    │   │   ├── fetch_adzuna_jobs(skills, location) → API call
    │   │   ├── fetch_jooble_jobs(keywords)
    │   │   ├── fetch_remoteo_jobs()
    │   │   └── aggregate_jobs(queries) → Combine sources
    │   │   Dependencies: requests library, API keys
    │   │
    │   ├── 📄 resume_parser.py
    │   │   Class: ResumeParser
    │   │   Methods:
    │   │   ├── extract_from_pdf(file_content) → Read PDF
    │   │   ├── extract_from_docx(file_content) → Read DOCX
    │   │   └── parse_resume(file_content, filename) → Full process
    │   │   Dependencies: PyPDF2, python-docx, SkillMatcher
    │   │
    │   ├── 📄 skill_matcher.py
    │   │   Class: SkillMatcher
    │   │   Methods:
    │   │   ├── extract_skills_from_text(text) → Find skills
    │   │   ├── calculate_match_score(...) → % match
    │   │   └── rank_jobs(jobs, user_skills) → Sort by score
    │   │   Dependencies: Regex, NLTK
    │   │
    │   ├── 📄 advanced_nlp.py
    │   │   Class: AdvancedSkillMatcher
    │   │   Methods:
    │   │   ├── extract_skills_nlp(text) → NLP-based extraction
    │   │   ├── calculate_tfidf_similarity(...) → Vector similarity
    │   │   └── rank_jobs_advanced(jobs, user_skills) → Hybrid rank
    │   │   
    │   │   Class: ResumeAnalyzer
    │   │   Methods:
    │   │   ├── extract_experience_level(resume_text) → Years
    │   │   └── extract_education(resume_text) → Degree
    │   │   Dependencies: scikit-learn, NLTK, numpy
    │   │
    │   ├── 📄 recommendation_service.py
    │   │   Class: RecommendationEngine
    │   │   Methods:
    │   │   ├── get_recommendations(user_id, top_n)
    │   │   └── personalized_score(job, user_profile)
    │   │
    │   └── 📄 scam_detection_service.py
    │       Class: ScamDetectionService
    │       Methods:
    │       ├── check_job(opportunity_id) → Is it flagged?
    │       └── report_job(opportunity_id, reason) → Add flag
    │
    └── 📁 instance/
        └── 📄 careertrust_dev.db
            SQLite database file (development only)
            Contains all tables and data
```

---

## 🔄 REQUEST FLOW Example

### **Example: Get Job Recommendations**

```
1. CLIENT REQUEST
   POST /api/jobs/recommendations
   Header: Authorization: Bearer JWT_TOKEN
   Body: {
     "skills": ["python", "react", "aws"],
     "top_n": 5
   }

2. FLASK ROUTING
   jobs_bp.route('/recommendations', methods=['POST'])
   @jwt_required()
   def get_job_recommendations():

3. JWT VALIDATION
   Extracts user_id from token

4. SERVICE LAYER
   a) Get all Opportunity records from DB
   b) For each job:
      - Extract requirements/description skills
      - Calculate SkillMatcher.basic_match_score()
      - Calculate AdvancedSkillMatcher.tfidf_similarity()
      - Combine: 60% basic + 40% TF-IDF
   c) Sort by final score (DESC)
   d) Return top N jobs

5. RESPONSE
   {
     "success": true,
     "recommendations": [
       {
         "id": 1,
         "title": "Senior Python Developer",
         "company": "TechCorp",
         "match_score": 87.5,
         "trust_score": 95,
         "matched_skills": ["python", "aws"],
         "missing_skills": ["kubernetes"],
         ...
       },
       ...
     ]
   }

6. CLIENT CALLBACK
   React component receives data
   Displays formatted recommendation cards
   User can save/bookmark jobs
```

---

## 🧪 Data Flow for Resume Upload

```
USER UPLOADS RESUME
       ↓
POST /api/profile/resume
(file: resume.pdf, Content-Type: multipart/form-data)
       ↓
ROUTE HANDLER (profile.py)
  get_resume()
  ├─ Check authorization (JWT)
  ├─ Get uploaded file
  └─ Call ResumeParser.parse_resume()
       ↓
RESUME PARSER SERVICE
  parse_resume(file_content, filename)
  ├─ If .pdf → extract_from_pdf()
  │  └─ Use PyPDF2 to read PDF text
  ├─ If .docx → extract_from_docx()
  │  └─ Use python-docx to read DOCX text
  └─ Extract text
       ↓
SKILL EXTRACTION
  SkillMatcher.extract_skills_from_text()
  ├─ Find 50+ predefined skills via regex
  └─ Return skill list
       ↓
NLP ANALYSIS (AdvancedSkillMatcher)
  ResumeAnalyzer.extract_experience_level()
  ├─ Find patterns like "5 years of experience"
  └─ Parse experience_years
  
  ResumeAnalyzer.extract_education()
  ├─ Find "Bachelor", "Master", "PhD"
  └─ Parse education level
       ↓
SAVE TO DATABASE
  user.resume_text = full_text
  user.resume_skills = skill_list
  user.experience_years = extracted_years
  db.session.commit()
       ↓
RESPONSE TO CLIENT
  {
    "success": true,
    "message": "Resume uploaded and parsed",
    "skills_extracted": ["python", "react", "fastapi", ...],
    "experience_years": 5,
    "education": "Bachelor"
  }
```

---

## 🎯 Key Service Dependencies

```
Routes Layer
    ↓
Services Layer
    ├─ JobAggregator
    │  └─ Needs: Opportunity model, requests library
    │
    ├─ SkillMatcher
    │  └─ Needs: Regex, NLTK, basic_keywords
    │
    ├─ AdvancedSkillMatcher + ResumeAnalyzer
    │  └─ Needs: scikit-learn, NLTK, numpy
    │
    ├─ ResumeParser
    │  └─ Needs: PyPDF2, python-docx, SkillMatcher
    │
    ├─ RecommendationEngine
    │  └─ Needs: Opportunity, User, SkillMatcher
    │
    └─ ScamDetectionService
       └─ Needs: ScamReport model, pattern matching
    ↓
Models Layer (SQLAlchemy)
    ├─ User
    ├─ Opportunity
    ├─ SavedJob
    ├─ Application
    └─ ScamReport
    ↓
Database (SQLite/PostgreSQL)
```

---

## 📊 Database Relationships

```
USERS (1) ─────────┐
                   │ many-to-many
                   │ (through SavedJob)
OPPORTUNITIES (1) ─┤
                   │ many-to-many
                   │ (through Application)
                   │
          ┌────────┴─────────┐
          ↓                  ↓
      SavedJob        Application
    (Bookmarks)     (Applications)

OPPORTUNITIES (1) ─── (many) SCAM_REPORTS
                            (Reports)
```

---

## 🔑 Key Algorithms Summary

### **1. Skill Matching (SkillMatcher)**
```python
def calculate_match_score(user_skills, job_description):
    # Extract skills from job description
    job_skills = extract_skills(job_description)
    
    # Count matches
    matches = len(user_skills ∩ job_skills)
    total = len(job_skills)
    
    # Return percentage
    return (matches / total) * 100 if total > 0 else 0
```

### **2. TF-IDF Similarity (AdvancedSkillMatcher)**
```python
def calculate_tfidf_similarity(user_skills, job_description):
    # Vectorize user skills
    user_vector = TfidfVectorizer.fit_transform([" ".join(user_skills)])
    
    # Vectorize job description
    job_vector = TfidfVectorizer.fit_transform([job_description])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(user_vector, job_vector)
    
    # Return as percentage
    return similarity[0][0] * 100
```

### **3. Hybrid Scoring (Job Recommendations)**
```python
def final_match_score(basic_score, tfidf_score):
    return (0.6 * basic_score) + (0.4 * tfidf_score)
```

---

## ✅ Implementation Status

### **COMPLETED** ✅
- ✅ All 18+ API endpoints designed & implemented
- ✅ Authentication (JWT) working
- ✅ User profile management functional
- ✅ Database schema synchronized
- ✅ Job recommendations with dual algorithm
- ✅ Resume parsing (PDF/DOCX) working
- ✅ Analytics dashboard functional
- ✅ Scam detection framework in place

### **TODO** ⏳
- ⏳ React frontend components
- ⏳ Unit/integration tests
- ⏳ Production deployment (Docker, PostgreSQL)
- ⏳ Email notifications
- ⏳ Performance optimization (caching, pagination)

---

*Document Created: April 12, 2026*
