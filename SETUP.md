# CareerTrust Project Setup Guide

## Overview
This is a complete setup guide for the CareerTrust project. Follow the steps below to get the project running.

## Project Structure
```
Career Trust/
├── backend/              # Flask API server
├── frontend/             # React.js web application
├── ml_models/            # Machine learning models
├── database/             # Database schemas and migrations
├── docs/                 # Documentation
├── tests/                # Test suite
└── .env.example          # Environment variables template
```

## Prerequisites
- Python 3.9+ (for backend) - ✅ Python 3.14.2 detected
- Node.js 16+ (for frontend)
- PostgreSQL 12+ (for database) - Optional (SQLite used by default for development)
- Git (for version control) - Optional

## Step 1: Database Setup (Optional for Development)

### Quick Start (SQLite - Recommended for Development)
Database is automatically created when backend starts. Skip PostgreSQL setup if you just want to test locally.

### Production Setup (PostgreSQL - Optional)
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run installer with default settings
3. Note the password you set for postgres user
4. Open PowerShell and connect:
   ```powershell
   psql -U postgres
   ```
5. Create database:
   ```sql
   CREATE DATABASE careertrust_dev;
   \c careertrust_dev
   \i 'C:/Users/kumar/Downloads/Career Trust/database/schema.sql'
   \q
   ```
6. Update `.env` file with PostgreSQL connection string

## Step 2: Backend Setup (✅ COMPLETED)

**Status**: Backend is running at http://localhost:5000

```powershell
cd "C:\Users\kumar\Downloads\Career Trust\backend"

# Create virtual environment
py -m venv venv

# Activate virtual environment
.\venv\Scripts\activate.bat

# Install dependencies
.\venv\Scripts\pip install -r requirements.txt

# Run the server
.\venv\Scripts\python app.py
```

Backend server running at: **http://localhost:5000**
- Database: SQLite (careertrust_dev.db) - auto-created
- All API endpoints are ready
- Hot reload enabled for development

## Step 3: Frontend Setup

```powershell
cd "C:\Users\kumar\Downloads\Career Trust\frontend"

# Install dependencies (including Tailwind CSS)
npm install

# Start development server
npm start
```

Frontend application will open at: **http://localhost:3000**

**Note**: The first `npm start` may take a moment to compile Tailwind CSS. If styling doesn't appear:
1. Wait for the build to complete (check the terminal)
2. Hard refresh browser: `Ctrl+Shift+R` (Windows)
3. Check browser console for any errors: `F12`
4. Delete node_modules and reinstall: `rm -r node_modules && npm install`

## Step 4: Verify Installation

### Check Backend is Running
```powershell
# In another terminal, test API endpoint
curl -X GET http://localhost:5000/api/opportunities `
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "total": 0,
  "pages": 0,
  "current_page": 1,
  "opportunities": []
}
```

### Check Frontend is Running
Open browser and visit: **http://localhost:3000**

You should see:
- ✅ CareerTrust header with navigation
- ✅ Welcome message and hero section with proper styling
- ✅ Feature cards with colors
- ✅ All buttons and links functional

### Test API - Register User
```powershell
curl -X POST http://localhost:5000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

Expected response (201 Created):
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

## Step 5: Create Test Data (Optional)

### Via API (Recommended)
```powershell
# First, register and login to get token
$loginResponse = curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }' | ConvertFrom-Json

$token = $loginResponse.access_token

# Create opportunity
curl -X POST http://localhost:5000/api/opportunities `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{
    "title": "Junior Developer",
    "company": "Tech Startup Inc",
    "description": "We are hiring a junior developer for our web team.",
    "job_type": "internship",
    "location": "San Francisco, CA",
    "salary": "$18/hour",
    "source": "LinkedIn"
  }'
```

### Direct Database (SQLite)
```powershell
# View database
# Navigate to: C:\Users\kumar\Downloads\Career Trust\backend\careertrust_dev.db
# Use SQLite browser or DBeaver to inspect tables
```

## Troubleshooting

### Frontend Styling Not Showing
1. Hard refresh browser: `Ctrl+Shift+R` 
2. Wait for npm to finish compiling (check terminal for "Compiled successfully")
3. Check browser console: `F12`
4. Clear cache: `npm cache clean --force`
5. Reinstall: `rm -r node_modules package-lock.json && npm install`

### Python Virtual Environment Issues
```powershell
# Use the batch file to activate (Windows PowerShell fix)
.\venv\Scripts\activate.bat

# NOT: .\venv\Scripts\Activate.ps1
```

### Port Already in Use
```powershell
# Find and kill process using port 5000 (Backend)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# For port 3000 (Frontend)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Backend Import Errors
- Ensure you're in the backend directory: `cd backend`
- Activate venv: `.\venv\Scripts\activate.bat`
- Reinstall: `pip install -r requirements.txt`

### Database Connection Error
- Development uses SQLite (auto-created at `careertrust_dev.db`)
- For PostgreSQL: Verify DATABASE_URL in `.env`
- Check PostgreSQL is running: Services app

### Module Not Found Errors
```powershell
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### NPM Issues
```powershell
# Clear cache and reinstall
npm cache clean --force
rm -r node_modules package-lock.json
npm install
```

## Next Steps

1. **Explore the API**: See `docs/API.md` for full endpoint documentation
2. **Implement Features**: Start with opportunity aggregation from one source
3. **Train ML Models**: Create training data for recommendation and scam detection
4. **Add Tests**: Write unit and integration tests in `tests/` directory
5. **Deploy**: Follow `docs/DEPLOYMENT.md` for production setup

## Development Commands

### Backend (PowerShell)
```powershell
cd backend

# Activate venv
.\venv\Scripts\activate.bat

# Run with auto-reload
.\venv\Scripts\python app.py

# Run tests (when available)
.\venv\Scripts\pytest tests/

# Deactivate when done
deactivate
```

### Frontend (PowerShell)
```powershell
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Clean/reinstall
npm cache clean --force && rm -r node_modules && npm install
```

### Database
```powershell
# SQLite (Development)
# Database file: C:\Users\kumar\Downloads\Career Trust\backend\careertrust_dev.db

# PostgreSQL (Production - if configured)
psql -U postgres -d careertrust_dev
```

## Documentation Files
- `README.md` - Project overview
- `docs/DEVELOPMENT.md` - Development guidelines
- `docs/DEPLOYMENT.md` - Production deployment
- `docs/API.md` - API documentation
- `database/schema.sql` - Database schema
- `database/migrations.md` - Migration guide

## Support
For issues or questions:
1. Check troubleshooting section above
2. Review relevant documentation
3. Check project GitHub issues (if available)

## License
MIT License

---

**Important**: Always keep your `.env` file secure and never commit it to version control!
