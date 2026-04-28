# Email Notifications & Scheduler Setup Guide

## Overview
The CareerTrust notification system automatically sends email alerts and digests to users about job matches. It uses APScheduler to run background jobs that check for matches and send emails on a schedule.

## Architecture

### Components
1. **NotificationService** (`app/services/notification_service.py`)
   - Email sending via SMTP
   - Job matching and scoring
   - Digest generation
   - Settings management

2. **Background Scheduler** (APScheduler)
   - Runs 3 continuous jobs in the background
   - Hourly alerts: Checks for new matches every hour
   - Daily digest: Sends at 08:00 UTC daily
   - Weekly digest: Sends Monday at 08:30 UTC

3. **Notification API** (`app/routes/notifications.py`)
   - GET `/api/notifications/settings` - Fetch user preferences
   - POST `/api/notifications/settings` - Update preferences
   - POST `/api/notifications/test-email` - Send test email
   - POST `/api/notifications/digest` - Manually trigger digest

## Step 1: Configure SMTP Environment Variables

### Option A: Using Mailtrap (Recommended for Development)
1. Sign up for free at [mailtrap.io](https://mailtrap.io)
2. Get SMTP credentials from your inbox
3. Update `.env` file:
```
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USERNAME=your_mailtrap_username
SMTP_PASSWORD=your_mailtrap_password
NOTIFICATIONS_FROM_EMAIL=noreply@careertrust.local
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### Option B: Using Gmail
1. Enable 2-factor authentication on your Gmail account
2. Generate an app-specific password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Update `.env` file:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
NOTIFICATIONS_FROM_EMAIL=your_email@gmail.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### Option C: Using SendGrid
1. Sign up at [sendgrid.com](https://sendgrid.com)
2. Create an API key
3. Update `.env` file:
```
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_sendgrid_api_key
NOTIFICATIONS_FROM_EMAIL=noreply@careertrust.local
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

## Step 2: Create Test User with Email Preferences

The Flask server must be running. In a new terminal:

```bash
cd backend
python setup_notifications.py
```

This script will:
- Create a test user: `test@careertrust.local`
- Enable email notifications
- Set up user profile with skills and interests
- Display the user ID for authentication

Example output:
```
✅ Notification preferences enabled:
   - Email Alerts: True
   - Digest Frequency: daily
   - Email: test@careertrust.local
   - Skills: Python, JavaScript, React, SQL, Machine Learning

📋 Test user ready:
   - User ID: 1
   - Email: test@careertrust.local
   - Username: testuser
```

## Step 3: Authenticate and Get JWT Token

Use the test user credentials to get a JWT token:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@careertrust.local","password":"password"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "test@careertrust.local",
    "username": "testuser"
  }
}
```

Save the `access_token` for the next steps.

## Step 4: Test Notification Endpoints

### 4a. Get Current Notification Settings
```bash
curl http://localhost:5000/api/notifications/settings \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "email_alerts": true,
  "digest_frequency": "daily",
  "digest_day": "monday",
  "digest_time": "08:00",
  "email": "test@careertrust.local",
  "last_alert_sent_at": null,
  "last_digest_sent_at": null
}
```

### 4b. Send Test Email
Verify SMTP is working by sending a test email:

```bash
curl -X POST http://localhost:5000/api/notifications/test-email \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "success": true,
  "message": "Test email sent to test@careertrust.local"
}
```

Check your email inbox (or Mailtrap inbox) for the test email.

### 4c. Manually Trigger Digest
```bash
curl -X POST http://localhost:5000/api/notifications/digest \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"frequency":"daily"}'
```

Response:
```json
{
  "sent": true,
  "message": "Email sent",
  "jobs_count": 5
}
```

### 4d. Update Notification Preferences
```bash
curl -X POST http://localhost:5000/api/notifications/settings \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email_alerts": true,
    "digest_frequency": "weekly",
    "digest_day": "monday",
    "digest_time": "09:00",
    "email": "test@careertrust.local"
  }'
```

## How the Scheduler Works

### Background Jobs

The APScheduler runs 3 continuous jobs:

#### 1. Hourly Alerts (Every Hour)
```python
run_alerts() 
  → For each user with email_alerts=true
    → Get new job matches from past 24 hours
    → Send alert email with top 5 matches
    → Update last_alert_sent_at timestamp
```

#### 2. Daily Digest (08:00 UTC)
```python
run_daily_digests()
  → For each user with digest_frequency="daily"
    → Get job matches from past day (7 for weekly)
    → Generate formatted digest email
    → Send to user's configured email
    → Update last_digest_sent_at timestamp
```

#### 3. Weekly Digest (Monday 08:30 UTC)
```python
run_weekly_digests()
  → For each user with digest_frequency="weekly"
    → Get job matches from past week
    → Generate weekly digest email
    → Send to user's configured email
    → Update last_digest_sent_at timestamp
```

### Job Matching Algorithm

For each job, the system:
1. Calculates match score based on user skills vs job requirements
2. Filters by user preferences:
   - Location preferences
   - Job type (full-time, contract, etc.)
   - Remote-only preference
   - Salary range
   - Preferred job sources
3. Ranks by match score (highest first)
4. Returns top results (5 for alerts, 10 for digests)

### Workflow Diagram

```
User Profile Created
    ↓
preferences.notifications.email_alerts = true
    ↓
APScheduler starts 3 background jobs
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│ Hourly Job      │ Daily Job       │ Weekly Job      │
│ Every 1 hour    │ Every day 08:00 │ Mon 08:30 UTC   │
└─────────────────┴─────────────────┴─────────────────┘
    ↓                   ↓                   ↓
Query recent jobs   Query recent jobs   Query recent jobs
    ↓                   ↓                   ↓
Score against user  Score against user  Score against user
    ↓                   ↓                   ↓
Send alert email    Send digest email    Send digest email
(5 matches)         (10 matches)         (10 matches)
    ↓                   ↓                   ↓
Update timestamps
    ↓
Email delivered to user's inbox
```

## Monitoring

Check the Flask dev server logs for scheduler activity:

```
[2026-04-28 08:00:00] Running daily digest job...
[2026-04-28 08:00:01] Processing user: testuser (ID: 1)
[2026-04-28 08:00:02] Found 5 matching jobs
[2026-04-28 08:00:03] Email sent to test@careertrust.local
```

## Troubleshooting

### Issue: "SMTP is not configured"
**Solution**: Check that all SMTP environment variables are set in `.env` file:
```bash
SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
```

### Issue: Email not sending
**Solution**: 
1. Verify SMTP credentials are correct
2. Test with `/api/notifications/test-email` endpoint
3. Check email inbox spam folder
4. Verify `email_alerts` is `true` in user preferences

### Issue: Scheduler not running
**Solution**:
1. Check Flask server logs for errors during startup
2. Verify APScheduler was installed: `pip install APScheduler`
3. Make sure no import errors in `app/services/notification_service.py`

### Issue: Jobs not matched
**Solution**:
1. Verify user has skills and interests set
2. Verify job opportunities exist in database
3. Check job requirements contain relevant keywords
4. Lower match score threshold in `NotificationService.get_matching_jobs()`

## Configuration Reference

### User Preference Fields
```python
preferences = {
  'notifications': {
    'email_alerts': bool,              # Enable/disable alerts
    'digest_frequency': 'daily'|'weekly',  # Daily or weekly digest
    'digest_day': 'monday'|'tuesday'|...,  # Day for weekly digest
    'digest_time': '08:00',            # Time in HH:MM format (UTC)
    'email': 'user@example.com',       # Email to send to
    'last_alert_sent_at': '2026-04-28T08:00:00',  # ISO timestamp
    'last_digest_sent_at': '2026-04-28T08:00:00'  # ISO timestamp
  }
}
```

### Environment Variables
```bash
# SMTP Configuration
SMTP_HOST=smtp.provider.com
SMTP_PORT=587
SMTP_USERNAME=username
SMTP_PASSWORD=password
NOTIFICATIONS_FROM_EMAIL=noreply@careertrust.local
SMTP_USE_TLS=true|false
SMTP_USE_SSL=true|false

# Digest Timing (Cron format)
# Daily digest time (format: HH:MM UTC)
# Weekly digest day and time (day 0=Monday, time HH:MM UTC)
```

## Next Steps

1. ✅ Configure SMTP environment variables
2. ✅ Create test user with notifications
3. ✅ Test email endpoints
4. 🔄 Integrate notification settings UI in React frontend
5. 🔄 Add notification status to dashboard
6. 🔄 Create email templates for better formatting

## Support

For issues or questions, check:
- Server logs in terminal running Flask
- Email provider logs (Mailtrap, Gmail, etc.)
- User preferences: `User.preferences['notifications']`
- Scheduler status: APScheduler console output
