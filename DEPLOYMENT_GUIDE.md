# CareerTrust Deployment Guide - Render + Netlify

## Deployment Architecture

```
┌─────────────────────┐
│  Frontend (React)   │
│   Deployed to       │
│   Netlify CDN       │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ API calls to │
    │  Render.com  │
    └──────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Backend (Flask + APScheduler)  │
│  Deployed to Render             │
│  - PostgreSQL Database          │
│  - Gunicorn WSGI Server         │
│  - Background Jobs Running      │
└─────────────────────────────────┘
```

---

## Part 1: Deploy Backend to Render

### Prerequisites
- Render.com account (free tier available)
- GitHub repository with your CareerTrust code

### Step 1: Push Code to GitHub

```bash
cd Career\ Trust
git init
git add .
git commit -m "Initial CareerTrust deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/careertrust.git
git push -u origin main
```

### Step 2: Create PostgreSQL Database on Render

1. Go to [render.com](https://render.com)
2. Click **New** → **PostgreSQL**
3. Fill in:
   - **Name:** `careertrust-db`
   - **Database:** `careertrust`
   - **User:** `postgres`
   - **Region:** Choose closest to you
   - **Plan:** Free tier
4. Click **Create Database**
5. Copy the **Internal Database URL** (starts with `postgres://`)

### Step 3: Create Web Service for Backend

1. Click **New** → **Web Service**
2. Select your GitHub repository
3. Fill in:
   - **Name:** `careertrust-backend`
   - **Runtime:** Python 3.11
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Region:** Same as database
   - **Plan:** Free tier
4. Click **Create Web Service**

### Step 4: Add Environment Variables

In Render dashboard for your web service:
1. Go to **Environment**
2. Add these variables:

```
FLASK_ENV=production
DATABASE_URL=<paste your database URL from step 2>
SECRET_KEY=<generate a random string>
JWT_SECRET_KEY=<generate a random string>
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
NOTIFICATIONS_FROM_EMAIL=your_email@gmail.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

3. Click **Save Changes**
4. The service will redeploy

### Step 5: Verify Backend Deployment

```bash
# Test your API
curl https://careertrust-backend.onrender.com/api/auth/login -X OPTIONS

# Should return: 200 OK
```

Note your backend URL (e.g., `https://careertrust-backend.onrender.com`) - you'll need this for frontend deployment.

---

## Part 2: Deploy Frontend to Netlify

### Prerequisites
- Netlify account (free tier available)
- GitHub repository (same as backend)

### Step 1: Build Frontend Locally (Optional Test)

```bash
cd frontend
npm install
npm run build

# This creates a 'build' folder ready for deployment
```

### Step 2: Create Netlify Site

1. Go to [netlify.com](https://netlify.com)
2. Click **Add new site** → **Import an existing project**
3. Select **GitHub**
4. Authorize Netlify to access your GitHub
5. Select your `careertrust` repository
6. Click **Deploy**

### Step 3: Configure Build Settings

Netlify auto-detects React settings, but verify:
1. **Build command:** `npm run build`
2. **Publish directory:** `build`
3. Click **Deploy**

### Step 4: Set Environment Variables

1. Go to **Site settings** → **Build & deploy** → **Environment**
2. Click **Edit variables**
3. Add:
   ```
   REACT_APP_API_URL=https://careertrust-backend.onrender.com/api
   ```
4. Save and redeploy

Or manually trigger redeploy:
1. Go to **Deploys**
2. Click **Trigger deploy**

### Step 5: Verify Frontend Deployment

- Your frontend is now at: `https://careertrust.netlify.app` (or custom domain)
- Test by:
  1. Opening the site in browser
  2. Try to log in
  3. Check browser console for any errors

---

## Environment Variables Checklist

### Backend (Render)
- [ ] `FLASK_ENV=production`
- [ ] `DATABASE_URL` (PostgreSQL URL from Render)
- [ ] `SECRET_KEY` (random string)
- [ ] `JWT_SECRET_KEY` (random string)
- [ ] `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`
- [ ] `NOTIFICATIONS_FROM_EMAIL`
- [ ] `SMTP_USE_TLS=true`

### Frontend (Netlify)
- [ ] `REACT_APP_API_URL=https://careertrust-backend.onrender.com/api`

---

## Post-Deployment Setup

### 1. Create First User

```bash
# Option A: Via Frontend
# Navigate to Register page, create account

# Option B: Via API
curl -X POST https://careertrust-backend.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your_email@gmail.com",
    "username": "your_username",
    "password": "your_password"
  }'
```

### 2. Configure Notification User

```bash
# SSH into Render (if available) or use one-off command:
# In Render dashboard → Web Service → Shell

python
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='your_email@gmail.com').first()
    if user:
        user.preferences = {
            'notifications': {
                'email_alerts': True,
                'digest_frequency': 'daily',
                'email': user.email
            }
        }
        db.session.commit()
        print("Notifications enabled!")
```

### 3. Test Email Sending

```bash
curl -X POST https://careertrust-backend.onrender.com/api/notifications/test-email \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

---

## Troubleshooting

### Backend Won't Start
- Check Render logs: Dashboard → Web Service → Logs
- Common issues:
  - Missing DATABASE_URL → Add to environment variables
  - Missing SMTP credentials → Add SMTP variables
  - Python version mismatch → Ensure 3.11+

### Frontend Shows "Cannot GET /"
- Check Netlify build logs
- Verify `netlify.toml` exists in root of frontend folder
- Try manual redeploy

### API Connection Issues
- Verify `REACT_APP_API_URL` is correct in Netlify
- Check CORS is enabled in Flask (should be via `Flask-CORS`)
- Test backend directly: `curl https://careertrust-backend.onrender.com/api/auth/login -X OPTIONS`

### Database Connection Failed
- Check DATABASE_URL format: should start with `postgresql://`
- Verify database is running in Render
- Try connecting with `psql` command

### Notifications Not Sending
- Verify SMTP credentials in Render environment
- Check Flask logs for scheduler errors
- Test with `/api/notifications/test-email` endpoint

---

## Monitoring & Updates

### Check Backend Health
```bash
curl https://careertrust-backend.onrender.com/api/auth/login -X OPTIONS -v
```

### View Logs
- **Render:** Dashboard → Logs tab
- **Netlify:** Dashboard → Deploys → Deploy log

### Update Backend Code
```bash
git add .
git commit -m "Update message"
git push origin main
# Render auto-deploys on push
```

### Update Frontend Code
```bash
git add .
git commit -m "Update message"  
git push origin main
# Netlify auto-deploys on push
```

---

## Production Checklist

- [ ] Backend deployed to Render
- [ ] PostgreSQL database created and linked
- [ ] All environment variables set correctly
- [ ] Frontend deployed to Netlify
- [ ] API URL configured in frontend
- [ ] Test login works end-to-end
- [ ] Email notifications working
- [ ] Scheduler jobs running (check Render logs)
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled (automatic)
- [ ] Database backups configured

---

## Custom Domains (Optional)

### For Render Backend
1. Register domain (GoDaddy, Namecheap, etc.)
2. Render dashboard → Settings → Custom Domain
3. Add DNS records per Render instructions
4. Example: `api.careertrust.com`

### For Netlify Frontend
1. Netlify dashboard → Settings → Domain management
2. Add your domain
3. Update DNS records
4. Example: `careertrust.com` or `app.careertrust.com`

---

## Cost Estimate (Free Tier)

| Service | Cost | Limits |
|---------|------|--------|
| Render Web | Free | Limited hours/month |
| Render DB | Free | 256MB storage |
| Netlify | Free | 300 build minutes/month |
| Gmail SMTP | Free | 50/day emails |
| **Total** | **FREE** | Perfect for testing |

---

## Next Steps After Deployment

1. ✅ Set up custom domain
2. ✅ Configure email alerts for all users
3. ✅ Monitor Render logs for errors
4. ✅ Backup database regularly
5. ✅ Set up error tracking (Sentry)
6. ✅ Configure analytics
7. ✅ Scale to paid tiers if needed

---

## Support

For issues:
- **Render docs:** https://render.com/docs
- **Netlify docs:** https://docs.netlify.com
- **Flask docs:** https://flask.palletsprojects.com
- **React docs:** https://react.dev

Good luck with your deployment! 🚀
