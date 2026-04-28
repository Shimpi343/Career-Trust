# Deployment Configuration Summary

This document explains all the files created/modified to enable deployment to Render (backend) and Netlify (frontend).

---

## Backend Files Created/Modified

### 1. **wsgi.py** (NEW) 
- **Location:** `backend/wsgi.py`
- **Purpose:** Entry point for Gunicorn on production
- **Contains:** Flask app factory call with database initialization
- **Used by:** Render's start command `gunicorn wsgi:app`

### 2. **render.yaml** (NEW)
- **Location:** `backend/render.yaml`
- **Purpose:** Render deployment configuration
- **Contains:** Web service definition, build/start commands, environment variable definitions
- **Alternative:** Use via Render dashboard UI (you can skip this and configure in dashboard)

### 3. **Procfile** (NEW)
- **Location:** `backend/Procfile`
- **Purpose:** Process file for Render (similar to Heroku)
- **Contains:** `web: gunicorn wsgi:app`
- **Note:** Render reads this to know how to start the app

### 4. **requirements.txt** (MODIFIED)
- **Added:** `gunicorn>=21.0.0`
- **Purpose:** Gunicorn is WSGI server for production (Flask dev server won't work on Render)

### 5. **config.py** (MODIFIED)
- **Changed:** PostgreSQL URL parsing for SQLAlchemy 2.0+ compatibility
- **Fixes:** Converts `postgres://` to `postgresql://` (required by newer SQLAlchemy)
- **Affects:** Production database connections

### 6. **app.py** (MODIFIED)
- **Changed:** Added PORT environment variable support
- **Added:** FLASK_ENV check for debug mode
- **Line:** `app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))`

---

## Frontend Files Created/Modified

### 1. **netlify.toml** (NEW)
- **Location:** `frontend/netlify.toml`
- **Purpose:** Netlify deployment configuration
- **Contains:**
  - Build command: `npm run build`
  - Publish directory: `build`
  - Environment variable: `REACT_APP_API_URL`
  - SPA redirect: All routes → index.html (for React Router)

### 2. **api.js** (NO CHANGES NEEDED)
- **Location:** `frontend/src/api.js`
- **Status:** Already uses `process.env.REACT_APP_API_URL` ✅
- **Means:** Frontend will automatically use Render URL in production

---

## Root Directory Files Created/Modified

### 1. **.env.example** (MODIFIED)
- **Purpose:** Template showing all required environment variables
- **Usage:** Copy to `.env` locally, configure values
- **Contains:** Comments explaining each variable and provider options

### 2. **DEPLOYMENT_GUIDE.md** (NEW)
- **Purpose:** Complete step-by-step deployment guide
- **Contains:**
  - Architecture diagram
  - Render backend setup (PostgreSQL + Web Service)
  - Netlify frontend setup
  - Environment variable checklist
  - Post-deployment configuration
  - Troubleshooting guide
  - Monitoring & updates
  - Production checklist

### 3. **DEPLOYMENT_CHECKLIST.md** (NEW)
- **Purpose:** Quick reference checklist for deployment
- **Contains:**
  - Step-by-step verification points
  - Testing commands
  - Environment variable reference
  - Troubleshooting table
  - Success indicators

---

## How Deployment Works

### Local Development (Current)
```
Client (localhost:3000)
    ↓
Frontend React Dev Server
    ↓
API calls to http://localhost:5000/api
    ↓
Backend Flask Dev Server (python app.py)
    ↓
SQLite Database (careertrust_dev.db)
```

### Production Deployment (After Steps)
```
Client (https://careertrust.netlify.app)
    ↓
Netlify CDN (static React build)
    ↓ env var: REACT_APP_API_URL
API calls to https://careertrust-backend.onrender.com/api
    ↓
Render Web Service
    ↓ gunicorn wsgi:app
Gunicorn WSGI Server (Flask)
    ↓
PostgreSQL Database (on Render)

Plus: APScheduler running background jobs hourly/daily/weekly
```

---

## Environment Variables (Deployment)

### What Gets Set in Render Dashboard
```
FLASK_ENV=production
DATABASE_URL=postgresql://...
SECRET_KEY=<random>
JWT_SECRET_KEY=<random>
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@gmail.com
SMTP_PASSWORD=<app-password>
NOTIFICATIONS_FROM_EMAIL=your@gmail.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### What Gets Set in Netlify Dashboard
```
REACT_APP_API_URL=https://careertrust-backend.onrender.com/api
CI=false
```

---

## Key Changes Summary

| File | Type | Change | Reason |
|------|------|--------|--------|
| wsgi.py | NEW | Flask entry point | Gunicorn needs WSGI app |
| requirements.txt | UPDATED | Added gunicorn | Production server |
| config.py | UPDATED | PostgreSQL URL fix | SQLAlchemy 2.0 compat |
| app.py | UPDATED | PORT env var | Render assigns port dynamically |
| netlify.toml | NEW | Build config | Netlify deployment |
| .env.example | UPDATED | Clear env vars | User reference |
| Deployment docs | NEW | 2 guides | Step-by-step help |

---

## Deployment Flow Checklist

1. ✅ Backend files ready (wsgi.py, Procfile, render.yaml)
2. ✅ Frontend files ready (netlify.toml, api.js already has env var)
3. ✅ Environment variable templates created
4. ✅ Documentation complete

**Next Steps:**
1. Push to GitHub: `git add . && git commit -m "Add deployment configs" && git push`
2. Create Render PostgreSQL database (5 min)
3. Create Render Web Service (auto-deploys on push)
4. Create Netlify site (auto-builds and deploys on push)
5. Configure environment variables in both dashboards
6. Test endpoints with curl commands from guide

---

## Testing After Deployment

### Backend Health Check
```bash
curl https://careertrust-backend.onrender.com/api/auth/login -X OPTIONS -v
# Should return: 200 OK, CORS headers
```

### Frontend Load
```
https://careertrust.netlify.app
# Should load React app without errors in console
```

### End-to-End Test
1. Open frontend URL
2. Register new account
3. Login
4. Check that API calls go to Render (DevTools Network tab)

---

## Important Notes

- ⚠️ **Free tier limits:**
  - Render: 15 min auto-sleep if no web traffic (wakes on request)
  - Netlify: 300 build minutes/month
  - Both suitable for testing/demo

- ✅ **No code changes needed:**
  - All backend code works on Render as-is
  - Frontend already uses env variables
  - Scheduler runs automatically

- 🔒 **Security:**
  - Never commit `.env` file (use `.env.example`)
  - Secret keys should be random and unique per environment
  - SMTP password should be app password, not account password

- 📊 **Monitoring:**
  - Render: Dashboard → Logs tab
  - Netlify: Dashboard → Deploys tab
  - Both auto-redeploy on git push

---

## Support Files

1. **DEPLOYMENT_GUIDE.md** - Full step-by-step guide (5-10 min read)
2. **DEPLOYMENT_CHECKLIST.md** - Quick verification checklist
3. **.env.example** - Environment variable reference
4. **backend/wsgi.py** - Production entry point
5. **backend/Procfile** - Server configuration
6. **frontend/netlify.toml** - Frontend configuration

---

## Next Commands to Run

```bash
# 1. Install gunicorn locally (optional for testing)
pip install gunicorn

# 2. Test production configuration locally
export FLASK_ENV=production
export DATABASE_URL=sqlite:///careertrust_prod.db
gunicorn wsgi:app

# 3. Push to GitHub
git add backend/wsgi.py backend/Procfile backend/render.yaml
git add backend/requirements.txt backend/config.py backend/app.py
git add frontend/netlify.toml .env.example
git add DEPLOYMENT_GUIDE.md DEPLOYMENT_CHECKLIST.md
git commit -m "Add deployment configuration for Render + Netlify"
git push origin main

# 4. Then follow DEPLOYMENT_CHECKLIST.md for Render & Netlify setup
```

---

**Deployment configuration is complete!** ✅  
See **DEPLOYMENT_CHECKLIST.md** to get started.
