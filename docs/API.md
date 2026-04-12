# CareerTrust API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Include JWT token in Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Auth Endpoints

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}

Response: 201 Created
{
  "message": "User registered successfully",
  "user_id": 1
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 1
}
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer <access_token>

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "username": "username"
}
```

### Opportunity Endpoints

#### List Opportunities
```
GET /opportunities?page=1&per_page=20&type=internship

Response: 200 OK
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "opportunities": [
    {
      "id": 1,
      "title": "Junior Developer",
      "company": "Tech Company",
      "description": "...",
      "job_type": "internship",
      "location": "New York",
      "salary": "$15/hour",
      "trust_score": 95,
      "source": "LinkedIn"
    }
  ]
}
```

#### Get Opportunity Details
```
GET /opportunities/{id}

Response: 200 OK
{
  "id": 1,
  "title": "Junior Developer",
  "company": "Tech Company",
  "description": "...",
  "job_type": "internship",
  "location": "New York",
  "salary": "$15/hour",
  "requirements": "...",
  "deadline": "2024-12-31",
  "trust_score": 95,
  "source": "LinkedIn",
  "url": "https://..."
}
```

### Scam Detection Endpoint

#### Analyze Job Posting
```
POST /scam-detection/analyze
Content-Type: application/json

{
  "text": "Job posting text here..."
}

Response: 200 OK
{
  "trust_score": 85,
  "is_suspicious": false,
  "analysis": "No major red flags detected"
}
```

### Recommendation Endpoint

#### Get Personalized Recommendations
```
GET /recommendations
Authorization: Bearer <access_token>

Response: 200 OK
{
  "recommendations": [
    {
      "id": 1,
      "title": "Junior Backend Developer",
      "match_score": 92
    }
  ]
}
```

## Error Responses

```
400 Bad Request
{
  "error": "Missing required fields"
}

401 Unauthorized
{
  "error": "Invalid credentials"
}

404 Not Found
{
  "error": "Resource not found"
}

500 Internal Server Error
{
  "error": "Server error message"
}
```

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per user

## CORS
- Frontend URL: http://localhost:3000
- Production: Configure in config.py
