# Deployment Checklist

## ✅ Backend Deployment (Render)

### Prerequisites
- [ ] GitHub account with repo pushed
- [ ] Render.com account (free tier)
- [ ] Gmail account with app password (for SMTP)

### Step-by-Step
- [ ] **Create Render PostgreSQL Database**
  - Go to render.com → New → PostgreSQL
  - Copy Internal Database URL
  - Wait for database to be available

- [ ] **Create Render Web Service**
  - New → Web Service → Select GitHub repo
  - Runtime: Python 3.11
  - Build command: `pip install -r requirements.txt`
  - Start command: `gunicorn wsgi:app`

- [ ] **Add Environment Variables to Render**
  ```
  FLASK_ENV=production
  DATABASE_URL=<from step 1>
  SECRET_KEY=<generate random>
  JWT_SECRET_KEY=<generate random>
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USERNAME=your_email@gmail.com
  SMTP_PASSWORD=your_app_password (NOT regular password)
  NOTIFICATIONS_FROM_EMAIL=your_email@gmail.com
  SMTP_USE_TLS=true
  SMTP_USE_SSL=false
  ```

- [ ] **Wait for Render Deployment to Complete**
  - Check Logs tab for "Listening on 0.0.0.0:3000"
  - Note your backend URL: `https://careertrust-backend.onrender.com`

- [ ] **Test Backend Deployment**
  ```bash
  curl https://careertrust-backend.onrender.com/api/auth/login -X OPTIONS -v
  # Should return: 200 OK
  ```

---

## ✅ Frontend Deployment (Netlify)

### Prerequisites
- [ ] Same GitHub repo with frontend code
- [ ] Netlify.com account (free tier)
- [ ] Backend URL from previous step

### Step-by-Step
- [ ] **Create Netlify Site**
  - Go to netlify.com → Add new site → Import existing project
  - Select GitHub repo
  - Build settings should auto-detect:
    - Build command: `npm run build`
    - Publish directory: `build`
  - Click Deploy

- [ ] **Add Environment Variables to Netlify**
  - Site settings → Build & deploy → Environment
  - Add variable:
    ```
    REACT_APP_API_URL=https://careertrust-backend.onrender.com/api
    ```

- [ ] **Trigger Redeploy**
  - Go to Deploys tab
  - Click "Trigger deploy"
  - Wait for build to complete (usually 2-3 minutes)
  - Note your frontend URL: `https://careertrust.netlify.app`

- [ ] **Test Frontend Deployment**
  - Open https://careertrust.netlify.app in browser
  - Check browser console (F12) for errors
  - Verify API calls are going to Render

---

## ✅ Post-Deployment Testing

- [ ] **Test User Registration**
  - Frontend: Use Register page
  - OR Backend API:
    ```bash
    curl -X POST https://careertrust-backend.onrender.com/api/auth/register \
      -H "Content-Type: application/json" \
      -d '{"email":"test@example.com","username":"testuser","password":"password123"}'
    ```

- [ ] **Test User Login**
  - Frontend: Use Login page
  - OR Backend API:
    ```bash
    curl -X POST https://careertrust-backend.onrender.com/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"test@example.com","password":"password123"}'
    ```

- [ ] **Test Email Notifications**
  - Get JWT token from login
  - Send test email:
    ```bash
    curl -X POST https://careertrust-backend.onrender.com/api/notifications/test-email \
      -H "Authorization: Bearer YOUR_JWT_TOKEN" \
      -H "Content-Type: application/json"
    ```
  - Check email inbox

- [ ] **Check Scheduler Status**
  - Render logs should show:
    ```
    APScheduler started
    Scheduler running with 3 jobs (hourly alerts, daily digest, weekly digest)
    ```

---

## ❌ Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend shows "Error R12" | Check if DATABASE_URL env var is set in Render |
| Frontend shows blank page | Check netlify.toml exists, manual redeploy |
| "Cannot connect to API" | Verify REACT_APP_API_URL is correct in Netlify |
| Emails not sending | Check SMTP credentials in Render, verify app password (not regular password) |
| Scheduler not running | Check Render logs for APScheduler startup messages |

---

## 🚀 Success Indicators

- [ ] Backend health check returns 200
- [ ] Frontend loads without errors
- [ ] Can register and login
- [ ] Emails send successfully
- [ ] Scheduler jobs running (check Render logs)

---

## 📊 Production Environment Variables Reference

### Backend (Render) - ALL REQUIRED
```
FLASK_ENV=production
DATABASE_URL=postgresql://...
SECRET_KEY=<random string>
JWT_SECRET_KEY=<random string>
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@gmail.com
SMTP_PASSWORD=<app password>
NOTIFICATIONS_FROM_EMAIL=your@gmail.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### Frontend (Netlify) - ALL REQUIRED
```
REACT_APP_API_URL=https://careertrust-backend.onrender.com/api
CI=false
```

---

## 💾 Backup & Monitoring

- [ ] **Set up database backups** (Render → Dashboard → Backups)
- [ ] **Enable notifications** (Render → Notifications tab)
- [ ] **Monitor logs regularly** (Render & Netlify dashboards)
- [ ] **Test email monthly** to ensure SMTP still works

---

## 🎉 Deployment Complete!

Your app is now live at:
- 🌐 Frontend: https://careertrust.netlify.app
- 🔌 Backend API: https://careertrust-backend.onrender.com/api
- 📊 Database: PostgreSQL on Render (internal)

Next steps:
1. Share URL with friends to test
2. Monitor logs for any issues
3. Plan migration to paid tiers if traffic grows
4. Set up custom domain (optional)
