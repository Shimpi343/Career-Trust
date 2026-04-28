# Render Deployment - Quick Setup Guide

## Step 1: Create PostgreSQL Database on Render

### 1a. Start the process
- Go to https://render.com/dashboard
- Click **New** → **PostgreSQL**

### 1b. Fill in database details
```
Name:           careertrust-db
Database:       careertrust
User:           postgres
Region:         [Choose closest to you - e.g., N. California]
Plan:           Free
```

### 1c. Click "Create Database"
- Wait 2-3 minutes for database to initialize
- You'll see green "Available" status

### 1d. **COPY THE DATABASE URL** ⭐
- Look for "Internal Database URL" section
- It should look like: `postgresql://postgres:PASSWORD@host:5432/careertrust`
- **SAVE THIS - you'll need it in Step 2**

---

## Step 2: Create Web Service for Backend

### 2a. Start the process
- In Render dashboard, click **New** → **Web Service**

### 2b. Connect GitHub Repository
- Click **Connect Repository**
- Select your repository: `careertrust` (or your repo name)
- Click **Connect**

### 2c. Fill in service details
```
Name:               careertrust-backend
Root Directory:     backend/
Runtime:            Python 3.11
Build Command:      pip install -r requirements.txt
Start Command:      gunicorn wsgi:app
Plan:               Free
Region:             [Same as database from Step 1]
```

### 2d. Click "Create Web Service"
- Render will now build and deploy your app
- Watch the "Logs" tab - wait for "Listening on 0.0.0.0:3000" message
- This takes ~2-3 minutes first time

---

## Step 3: Add Environment Variables

### 3a. Go to Environment Settings
- Web Service dashboard → **Environment** tab
- Click **Add Environment Variable** for each one below

### 3b. Add these variables one by one

#### Required Production Variables
```
Key: FLASK_ENV
Value: production

Key: DATABASE_URL
Value: [PASTE THE URL FROM STEP 1d - the postgresql:// URL]

Key: SECRET_KEY
Value: [Generate random: use https://1password.com/password-generator or run: python -c "import secrets; print(secrets.token_urlsafe(32))"]

Key: JWT_SECRET_KEY
Value: [Generate different random: python -c "import secrets; print(secrets.token_urlsafe(32))"]
```

#### SMTP Configuration (Email Notifications)
```
Key: SMTP_HOST
Value: smtp.gmail.com

Key: SMTP_PORT
Value: 587

Key: SMTP_USERNAME
Value: [YOUR GMAIL EMAIL - e.g., kumarishimpi362@gmail.com]

Key: SMTP_PASSWORD
Value: [YOUR GMAIL APP PASSWORD - NOT your regular password]
Note: Generate at https://myaccount.google.com/apppasswords

Key: NOTIFICATIONS_FROM_EMAIL
Value: [YOUR GMAIL EMAIL]

Key: SMTP_USE_TLS
Value: true

Key: SMTP_USE_SSL
Value: false
```

### 3c. Click "Save Changes"
- Render will restart the service with new variables
- Check logs to confirm startup successful

---

## Step 4: Verify Backend is Working

### 4a. Get your backend URL
- Web Service dashboard shows: **https://careertrust-backend.onrender.com** (or similar)
- Save this URL

### 4b. Test backend health
```bash
curl https://careertrust-backend.onrender.com/api/auth/login -X OPTIONS -v
```

**Expected response:**
```
HTTP/1.1 200 OK
access-control-allow-origin: *
access-control-allow-methods: GET, POST, PUT, DELETE, OPTIONS
```

If you get 502/503, check logs in Render dashboard - usually means missing env vars.

### 4c. Check scheduler is running
- Render dashboard → **Logs** tab
- Look for messages like:
```
APScheduler started
Scheduler running with 3 jobs
```

---

## Troubleshooting Common Issues

### "Application failed to start"
→ Check Logs tab for error messages
→ Most common: Missing DATABASE_URL env var
→ Solution: Add DATABASE_URL to Environment tab

### "502 Bad Gateway"
→ Backend crashed, check logs
→ Usually SMTP credentials issue
→ Verify SMTP variables are correct

### "Connection to database failed"
→ PostgreSQL database not ready
→ Wait 2-3 minutes after creating database
→ Or recreate database

### "ImportError: No module named..."
→ Missing Python package
→ Run locally: `pip install -r requirements.txt`
→ Commit & push changes to git
→ Render will rebuild automatically

---

## Environment Variable Reference

### Generate Random Secrets
Run this in your terminal:
```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY  
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Copy the 16-character password
4. Use in SMTP_PASSWORD field

---

## Next Steps After Render Setup

✅ Backend is deployed and running

Next: Deploy Frontend to Netlify
→ See DEPLOYMENT_CHECKLIST.md Part 2

---

## Quick Checklist for This Section

- [ ] Created PostgreSQL database
- [ ] Copied database URL (Internal URL)
- [ ] Created Web Service
- [ ] Added all 11 environment variables
- [ ] Backend shows "Listening" in logs
- [ ] Health check returns 200 OK
- [ ] Saved backend URL (https://careertrust-backend.onrender.com)

---

## Command Reference

Test backend after it's deployed:
```bash
# Test CORS/health
curl https://careertrust-backend.onrender.com/api/auth/login -X OPTIONS -v

# Create test user
curl -X POST https://careertrust-backend.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Test123!"}'

# Login
curl -X POST https://careertrust-backend.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

---

**Estimated time:** 5-10 minutes total

Questions? See DEPLOYMENT_GUIDE.md for more details.
