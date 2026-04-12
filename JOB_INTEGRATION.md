# Job Integration System Documentation

## Overview
CareerTrust now supports fetching real job opportunities from three different sources:
- **GitHub Jobs** (Free, no authentication required)
- **Indeed** (Requires API key)
- **LinkedIn** (Requires credentials)

## Features

### 1. GitHub Jobs Integration
- **Status**: ✅ Ready to use immediately
- **API**: Free public API, no authentication needed
- **Limitations**: Limited job categories (mostly tech), updates less frequently
- **How to use**: Just search for a job title and fetch

### 2. Indeed Integration
- **Status**: Available (requires API key)
- **API**: Official Indeed API
- **Requires**: `INDEED_API_KEY` environment variable
- **Setup**: https://opensource.indeedeng.io/api-documentation/
- **How to enable**:
  ```bash
  # Set environment variable
  export INDEED_API_KEY=your_api_key_here
  
  # Or on Windows (PowerShell)
  $env:INDEED_API_KEY = "your_api_key_here"
  ```

### 3. LinkedIn Integration
- **Status**: Available (requires credentials)
- **Requires**: 
  - `LINKEDIN_EMAIL` environment variable
  - `LINKEDIN_PASSWORD` environment variable
  - `linkedin-api` Python package installed
- **Installation**:
  ```bash
  pip install linkedin-api
  ```
- **How to enable**:
  ```bash
  export LINKEDIN_EMAIL=your.email@gmail.com
  export LINKEDIN_PASSWORD=your_password
  ```
- **Note**: LinkedIn frequently updates its blocking policies. This integration uses an unofficial API.

## API Endpoints

### 1. Get Available Sources
```
GET /api/jobs/sources
```
Returns status of all three job sources.

**Response**:
```json
{
  "success": true,
  "sources": {
    "github_jobs": {
      "name": "GitHub Jobs",
      "status": "available",
      "requires_auth": false
    },
    "indeed": {
      "name": "Indeed",
      "status": "requires_config",
      "requires_auth": true
    },
    "linkedin": {
      "name": "LinkedIn",
      "status": "requires_config",
      "requires_auth": true
    }
  }
}
```

### 2. Fetch from Specific Source
```
POST /api/jobs/fetch/{source}
Authorization: Bearer {token}
Content-Type: application/json

{
  "search_term": "python developer",
  "location": "USA",
  "limit": 10
}
```

**Available sources**: `github_jobs`, `indeed`, `linkedin`

**Response**:
```json
{
  "success": true,
  "source": "github_jobs",
  "count": 10,
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "San Francisco",
      "description": "...",
      "job_url": "https://...",
      "job_type": "Job",
      "source": "GitHub Jobs",
      "salary": null,
      "trust_score": 95
    }
  ]
}
```

### 3. Fetch from All Sources
```
POST /api/jobs/fetch
Authorization: Bearer {token}
Content-Type: application/json

{
  "search_term": "python",
  "limit_per_source": 5,
  "auto_add": false
}
```

**Parameters**:
- `search_term`: Job title to search (optional)
- `limit_per_source`: Max results per source (default: 10, max: 50)
- `auto_add`: Automatically add jobs to database (default: false)

**Response**:
```json
{
  "success": true,
  "sources": {
    "github_jobs": 10,
    "indeed": 5,
    "linkedin": 0
  },
  "total_jobs": 15,
  "aggregated": { /* all job data */ },
  "added_to_db": 0
}
```

### 4. Import Jobs to Database
```
POST /api/jobs/import
Authorization: Bearer {token}
Content-Type: application/json

{
  "jobs": [
    {
      "title": "Software Engineer",
      "company": "Tech Corp",
      "description": "...",
      "job_url": "https://...",
      "source": "GitHub Jobs",
      "job_type": "Job",
      "trust_score": 90,
      "salary": null,
      "location": "San Francisco",
      "posted_at": "2026-04-12T00:00:00"
    }
  ],
  "deduplicate": true
}
```

**Parameters**:
- `jobs`: Array of job objects
- `deduplicate`: Skip duplicate jobs (by title + company)

**Response**:
```json
{
  "success": true,
  "added": 10,
  "duplicates": 2,
  "errors": 0,
  "total_processed": 12
}
```

### 5. Preview Jobs Before Import
```
POST /api/jobs/preview
Authorization: Bearer {token}
Content-Type: application/json

{
  "jobs": [ /* job array */ ]
}
```

Returns validation results without modifying database.

## Frontend Usage

### Job Integration Page
Navigate to `/jobs/integration` to access the job import interface.

**Features**:
1. **Source Status Tab** - View availability of each job source
2. **Import Jobs Tab** - Fetch and import jobs
   - Search for specific job titles
   - Fetch from single source or all sources
   - Preview jobs before importing
   - Import with automatic deduplication

## Workflow

### Basic Workflow
1. Go to `/jobs/integration` page
2. Click "Fetch from Selected Source" or "Fetch from All Sources"
3. Review jobs in the preview
4. Click "Import All" to add to database
5. Jobs appear in Opportunities and can now be recommended

### With Search Term
1. Enter search term (e.g., "Python Developer")
2. Select source (GitHub Jobs is always available)
3. Click fetch
4. Import selected jobs

## Database Fields

All imported jobs are stored with:
- `title` - Job title
- `company` - Company name
- `description` - Full job description
- `location` - Job location
- `salary` - Salary range (if available)
- `job_type` - "Job", "Internship", "Hackathon"
- `source` - Source platform (GitHub Jobs, Indeed, LinkedIn)
- `trust_score` - Reliability score (0-100)
  - GitHub Jobs: 95 (trusted platform)
  - Indeed: 90 (trusted platform)
  - LinkedIn: 85 (professional network)
  - User submissions: 50 (need verification)
- `url` - Link to original job posting
- `created_at` - When added to CareerTrust
- `updated_at` - Last modification time

## Trust Scoring

Different sources get different default trust scores:
- **GitHub Jobs**: 95/100 (official, curated)
- **Indeed**: 90/100 (large, established platform)
- **LinkedIn**: 85/100 (professional network, occasional spam)
- **User Submitted**: 50/100 (needs verification)

These scores can be adjusted based on scam detection results.

## Environment Variables

Create a `.env` file in the backend directory:

```bash
# GitHub Jobs - No auth needed
# GITHUB_JOBS_ENABLED=true  # Always enabled

# Indeed Setup
INDEED_API_KEY=your_indeed_api_key

# LinkedIn Setup
LINKEDIN_EMAIL=your.email@gmail.com
LINKEDIN_PASSWORD=your_password

# Other configs
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

## Troubleshooting

### GitHub Jobs not returning results
- Check internet connection
- Verify search term is reasonable
- GitHub Jobs API has rate limits

### Indeed API errors
- Verify `INDEED_API_KEY` is set correctly
- Check API key has not expired
- Visit https://opensource.indeedeng.io/api-documentation/

### LinkedIn API not responding
- `linkedin-api` package works best with linkedin-api>=2.0.0
- LinkedIn frequently updates security
- If fails, fall back to `pip install --upgrade linkedin-api`
- Consider using manual CSV import as alternative

## Future Enhancements

1. **Scheduled Fetching** - Automatically fetch jobs daily
2. **Webhook Support** - Integrate with job boards' webhooks
3. **Advanced Filtering** - Filter by salary, experience level, etc.
4. **Duplicate Detection** - Smarter detection across sources
5. **Email Parsing** - Parse job emails automatically
6. **Custom Sources** - Add company career pages
7. **Caching** - Cache frequently requested searches

## Code Structure

```
backend/
├── app/
│   ├── services/
│   │   ├── job_integrations.py  # Integration classes
│   │   └── __init__.py
│   └── routes/
│       ├── jobs.py  # Job API endpoints
│       └── __init__.py

frontend/
└── src/
    └── pages/
        └── JobIntegration.js  # UI for importing jobs
```

## Testing

### Test GitHub Jobs (Free)
```bash
curl -X POST http://localhost:5000/api/jobs/fetch/github_jobs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"search_term": "python", "limit": 5}'
```

### Test Job Sources Status
```bash
curl http://localhost:5000/api/jobs/sources
```

## Tips

1. **Start with GitHub Jobs** - No configuration needed
2. **Set up Indeed** for job volume - Most comprehensive database
3. **Use LinkedIn** for professional contacts - Best for networking
4. **Always review jobs** before marking as approved
5. **Monitor trust scores** - Flag suspicious postings
6. **Use recommendations** - Match jobs to user skills

