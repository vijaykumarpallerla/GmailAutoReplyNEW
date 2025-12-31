# Gmail Auto-Reply Deployment Guide

## System Architecture

### Current Concurrency Model
```
APScheduler (Background Job)
├── ThreadPoolExecutor (max_workers=2)
│   ├── Thread 1: User 1, 3, 5, 7... (every 28 seconds)
│   └── Thread 2: User 2, 4, 6, 8... (every 28 seconds)
└── All 50 users processed sequentially across 2 threads
```

**For 50 users:** Each user waits ~15-30 seconds for their turn (depends on load)

### Google API Limits
- **Per user:** 10 requests/second
- **Your app:** ~2 requests per user per cycle (pull + profile)
- **50 users × 2 req/user / 28s interval = 3.5 requests/second** ✅
- **Conclusion: Google can EASILY handle 50 users!**

---

## Pre-Deployment Checklist

### 1. Local Testing
```bash
# Test with all features
python manage.py runserver
# Visit http://127.0.0.1:8000/ and test login, rules, emails
```

### 2. Create requirements.txt
```bash
pip freeze > requirements.txt
```

### 3. Create Procfile (Render needs this)
```
web: gunicorn gmail_auto_reply.wsgi
release: python manage.py migrate
```

### 4. Create runtime.txt (specify Python version)
```
python-3.13.2
```

### 5. Create .env.example (for documentation)
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgresql://user:pass@host/db
GMAIL_CLIENT_ID=xxx.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=xxx
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

---

## Step-by-Step Render Deployment

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

### 2. Connect GitHub Repository
- Create new "Web Service"
- Connect your GitHub repo
- Select branch: main

### 3. Configure Build & Deploy
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn gmail_auto_reply.wsgi
```

### 4. Set Environment Variables
Go to **Settings → Environment Variables** and add:
```
DEBUG=False
SECRET_KEY=<generate-random-secret>
ALLOWED_HOSTS=your-app-xyz.onrender.com
DATABASE_URL=postgresql://neondb_owner:...@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
GMAIL_CLIENT_ID=<from-google-cloud>
GMAIL_CLIENT_SECRET=<from-google-cloud>
CLOUDINARY_URL=cloudinary://378252628684391:...@dowbh5rfy
```

### 5. Update Google Cloud OAuth
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Select your project
3. **APIs & Services → Credentials**
4. Click your OAuth 2.0 Client ID
5. **Authorized redirect URIs** → Add:
   ```
   https://your-app-xyz.onrender.com/accounts/google/login/callback/
   ```
6. **Save**

### 6. Update Django Settings
File: `gmail_auto_reply/settings.py`

Add to bottom:
```python
# Render/Production Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_SECURITY_POLICY = {
        "default-src": ("'self'",),
    }
```

### 7. Deploy!
- Push to GitHub: `git push origin main`
- Render automatically deploys
- Watch logs: Render dashboard → Logs

---

## Post-Deployment

### 1. Run Database Migrations
```bash
# Render runs this automatically via Procfile "release" command
# Or manually:
heroku run python manage.py migrate --app your-app
# For Render:
```

### 2. Create Superuser
```bash
# Can't do interactive on Render, so:
# Use Django shell or admin endpoint
```

### 3. Test Live
- Visit `https://your-app-xyz.onrender.com/`
- Test Google Login
- Create test rule
- Send test email

---

## Scaling for 50+ Users

### Current Setup (Good for ~30-40 users)
```
Scheduler: 28 second interval
Threads: 2 max workers
Per cycle: ~56 seconds total for all users
```

### For 50+ Users - Options

**Option A: Increase Threads** (Simple)
File: `auto_reply/scheduler.py` (Line ~42)
```python
executors = {"default": ThreadPoolExecutor(max_workers=4)}  # Was 2
```
- More parallel processing
- More memory/CPU usage
- Faster for users

**Option B: Increase Interval** (Conservative)
File: `auto_reply/scheduler.py` (Line 36)
```python
interval_seconds = 60  # Was 28
```
- Less frequent checks
- Lower resource usage
- Slower response time

**Option C: User-Based Staggering** (Advanced)
Spread users across time:
```python
# User 1 checks at 0s, User 2 at 5s, User 3 at 10s, etc.
user_index = user.id % 10
delay = user_index * 5
# Then offset their scheduler
```

**Recommendation for 50 users:**
```python
executors = {"default": ThreadPoolExecutor(max_workers=4)}  # 4 threads
interval_seconds = 45  # 45 seconds
# Cost: ~4 Google API req/sec, ~100MB RAM, ~0.5 CPU
```

---

## Monitoring & Troubleshooting

### Check Logs
```bash
# Render logs (live)
# Dashboard → Your App → Logs tab

# Look for:
[DEBUG] gmail_pull_for_user called for user: xxx  # ✅ Good
[ERROR] Token refresh FAILED  # ⚠️ User needs to re-login
[ERROR] AUTHORIZATION FAILED  # ⚠️ Auth expired
Execution of job skipped  # ✅ Normal when busy
```

### Common Issues

**1. Google Login Not Working**
- ❌ OAuth redirect URL not updated in GCP
- ✅ Solution: Add `https://your-app.onrender.com/accounts/google/login/callback/` to GCP

**2. "Unauthorized" Errors Every 28s**
- ❌ Token refresh failing silently
- ✅ Solution: Check logs for `[ERROR] Token refresh FAILED`
- ✅ User needs to re-login

**3. Jobs Skipped Too Often**
- ❌ Interval too short for number of users
- ✅ Solution: Increase interval or threads

**4. Cloudinary 401 Errors**
- ❌ PDF uploaded as private
- ✅ Solution: Already fixed with `access_mode='public'`

**5. Database Connection Lost**
- ❌ Neon connection pool exhausted
- ✅ Solution: Render auto-recovers, but check Neon dashboard

---

## Environment Variables Explained

| Variable | Example | Purpose |
|----------|---------|---------|
| DEBUG | False | Production mode (no debug info) |
| SECRET_KEY | abc123... | Django encryption key |
| ALLOWED_HOSTS | your-app.onrender.com | Which domains can access |
| DATABASE_URL | postgresql://... | Neon database connection |
| GMAIL_CLIENT_ID | xxx.apps.google... | Google OAuth client |
| GMAIL_CLIENT_SECRET | xxx | Google OAuth secret |
| CLOUDINARY_URL | cloudinary://... | File storage connection |

---

## Performance Expectations

### With 50 Users (4 threads, 45s interval)

| Metric | Value | Status |
|--------|-------|--------|
| Response Time | 20-40 seconds | ✅ Good |
| Google API Calls/sec | ~4 | ✅ Safe |
| Memory Usage | ~150-200MB | ✅ Safe |
| CPU Usage | ~0.5 cores | ✅ Safe |
| Cloudinary Bandwidth | ~10GB/month | ⚠️ Watch (free = 1GB) |
| Render Cost | ~$7-15/month | ✅ Cheap |

---

## Disaster Recovery

### Backup Database
```bash
# Neon provides automated backups
# Dashboard → Backups → View
```

### Restore from Backup
```bash
# Contact Neon support or use their restore UI
```

### Clear Stuck Tokens
```bash
# If many users have auth failures:
python manage.py shell
>>> from auto_reply.models import GmailToken
>>> GmailToken.objects.all().delete()
# Users need to re-login
```

---

## Next Steps

1. ✅ Create `requirements.txt` and `Procfile`
2. ✅ Update GCP OAuth redirect URLs
3. ✅ Deploy to Render
4. ✅ Test with 5 users first
5. ✅ Monitor logs for 1 week
6. ✅ Scale to 50 users gradually
7. ✅ Upgrade Cloudinary if needed (for 50+ users)

---

## Support

Common errors and solutions in logs:
- Look for `[ERROR]` - something needs fixing
- Look for `[DEBUG]` - normal operation logging
- Scheduler skips are normal when busy
- Auth failures require user re-login

Good luck! 🚀
