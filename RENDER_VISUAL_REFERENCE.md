# Render Setup - Visual Reference

## What You'll See At Each Step

---

## ✅ Step 1: After Creating PostgreSQL Database

### In Render Dashboard:
```
careertrust-db
├─ Status: Available (green) ✓
├─ Type: PostgreSQL
├─ Region: N. California
└─ Connections
   └─ Internal Database URL: postgresql://postgres:[PASSWORD]@[HOSTNAME]:5432/careertrust
      ↑ THIS IS WHAT YOU NEED TO COPY
```

**Example Internal Database URL:**
```
postgresql://postgres:ABC123xyz@dpg-xxxxxx.aws.com:5432/careertrust
```

**Copy this exact string into DATABASE_URL environment variable later**

---

## ✅ Step 2: After Creating Web Service

### In Render Dashboard → Web Service:
```
careertrust-backend
├─ Status: Deploying... → Live (when ready)
├─ Runtime: Python 3.11
├─ Build Command: pip install -r requirements.txt
├─ Start Command: gunicorn wsgi:app
├─ URL: https://careertrust-backend.onrender.com ← YOUR API URL
└─ Logs: [Shows build progress]
```

**In Logs, you'll see:**
```
=== Collecting pip packages ===
Collecting Flask>=3.0.0
...
Successfully built Flask
Installing collected packages: Flask, flask-sqlalchemy, ...
Successfully installed ...

=== Activating Python Environment ===
...

=== Build succeeded ===
[12:34:56] Starting service with 'gunicorn wsgi:app'
...
[12:34:58] Listening on 0.0.0.0:3000
```

**When you see "Listening on 0.0.0.0:3000" → Setup was successful!**

---

## ✅ Step 3: After Adding Environment Variables

### In Render Dashboard → Web Service → Environment:

```
Variables
├─ FLASK_ENV: production
├─ DATABASE_URL: postgresql://postgres:ABC123xyz@...
├─ SECRET_KEY: [random string]
├─ JWT_SECRET_KEY: [random string]
├─ SMTP_HOST: smtp.gmail.com
├─ SMTP_PORT: 587
├─ SMTP_USERNAME: kumarishimpi362@gmail.com
├─ SMTP_PASSWORD: [16-char app password]
├─ NOTIFICATIONS_FROM_EMAIL: kumarishimpi362@gmail.com
├─ SMTP_USE_TLS: true
└─ SMTP_USE_SSL: false
```

**After you Save Changes:**
- Render will restart the service (takes ~30 seconds)
- Check Logs again - should see "Listening on 0.0.0.0:3000" again

---

## 📋 Copy-Paste Template

Use this template when adding environment variables. Replace bracketed values:

```
FLASK_ENV = production

DATABASE_URL = postgresql://postgres:[PASSWORD]@[HOSTNAME]:5432/careertrust

SECRET_KEY = [run: python -c "import secrets; print(secrets.token_urlsafe(32))"]

JWT_SECRET_KEY = [run: python -c "import secrets; print(secrets.token_urlsafe(32))"]

SMTP_HOST = smtp.gmail.com

SMTP_PORT = 587

SMTP_USERNAME = [your gmail: kumarishimpi362@gmail.com]

SMTP_PASSWORD = [from https://myaccount.google.com/apppasswords - 16 chars]

NOTIFICATIONS_FROM_EMAIL = [your gmail: kumarishimpi362@gmail.com]

SMTP_USE_TLS = true

SMTP_USE_SSL = false
```

---

## 🔍 How to Find Values

### DATABASE_URL
1. Render Dashboard
2. Click on `careertrust-db` (PostgreSQL)
3. Look for "Connections" section
4. Copy "Internal Database URL"

### Backend URL (after Web Service created)
1. Render Dashboard
2. Click on `careertrust-backend` (Web Service)
3. URL shown at top: `https://careertrust-backend.onrender.com`

### SECRET_KEY & JWT_SECRET_KEY
```bash
cd "C:\Users\kumar\Downloads\Career Trust\backend"
python generate_secrets.py
```

### SMTP_PASSWORD (Gmail)
1. Go to https://myaccount.google.com/apppasswords
2. Select: App = "Mail", Device = "Windows Computer"
3. Click "Generate"
4. Copy the 16-character password shown

---

## ✅ Test URLs (After Everything is Set Up)

**Health Check:**
```
https://careertrust-backend.onrender.com/api/auth/login
Method: OPTIONS
Expected: 200 OK
```

**Test Registration:**
```
https://careertrust-backend.onrender.com/api/auth/register
Method: POST
Body: {"email":"test@test.com","username":"testuser","password":"Test123!"}
Expected: 201 Created or similar
```

---

## ⏱️ Timeline

| Step | Task | Time |
|------|------|------|
| 1 | Create PostgreSQL | 2-3 min |
| 2 | Create Web Service | 3-5 min (building) |
| 3 | Add Environment Variables | 1-2 min |
| 4 | Service restarts | 30 sec |
| 5 | Verify in Logs | 1 min |
| **Total** | **Ready to deploy!** | **~10 min** |

---

## 🚨 Common Issues & Fixes

### "Build failed"
- **Check:** requirements.txt has correct packages
- **Fix:** Run locally: `pip install -r requirements.txt`
- **Then:** Commit and push changes

### "Application crashed" (after variables added)
- **Check:** All variables added correctly
- **Fix:** Go to Environment tab, verify DATABASE_URL has full URL
- **Then:** Click "Save Changes" again

### "503 Service Unavailable" (after testing API)
- **Check:** Backend URL is correct
- **Check:** Logs show "Listening on 0.0.0.0:3000"
- **Fix:** Wait 1-2 minutes, try again

### Can't find PostgreSQL URL
- **Where to look:**
  - Dashboard → Click `careertrust-db`
  - Look for "Connections" panel
  - Find "Internal Database URL" line

---

## Success Indicators

✅ PostgreSQL database shows "Available" (green)
✅ Web Service shows "Live" (green)
✅ Logs show "Listening on 0.0.0.0:3000"
✅ Health check returns 200 OK
✅ Next step: Deploy frontend to Netlify

See **RENDER_SETUP_QUICK_GUIDE.md** for step-by-step instructions.
