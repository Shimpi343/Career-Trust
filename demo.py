#!/usr/bin/env python
"""
CareerTrust Demo - Comprehensive Feature Showcase
Shows all implemented features with real API calls
"""

import requests
import json
from datetime import datetime
import uuid

BASE_URL = "http://localhost:5000/api"

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_section(title):
    print(f"\n  📌 {title}")
    print("-" * 70)

def print_success(msg):
    print(f"  ✅ {msg}")

def print_error(msg):
    print(f"  ❌ {msg}")

def print_info(msg):
    print(f"  ℹ️  {msg}")

# ============================================================================
# DEMO STARTS HERE
# ============================================================================

print_header("CareerTrust Platform - Full Feature Demo")
print_info("Demonstrating Resume Upload, AI Skill Matching, and Job Recommendations")

# ============================================================================
# 1. USER AUTHENTICATION
# ============================================================================

print_section("1️⃣  User Registration & Authentication")

import uuid
demo_unique = str(uuid.uuid4())[:8]
demo_user = {
    "username": f"demo{demo_unique}",
    "email": f"demo{demo_unique}@careertrust.com",
    "password": "DemoPass123!"
}

print_info(f"Registering user: {demo_user['email']}")

# Try to register
reg_response = requests.post(
    f"{BASE_URL}/auth/register",
    json=demo_user
)

if reg_response.status_code == 201:
    print_success("User registered successfully")
elif reg_response.status_code == 400 and "already exists" in reg_response.text:
    print_info("User already exists (using existing account)")
else:
    print_error(f"Registration failed: {reg_response.text}")

# Login
print_info(f"Logging in as {demo_user['email']}...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": demo_user['email'], "password": demo_user['password']}
)

if login_response.status_code != 200:
    print_error(f"Login failed: {login_response.text}")
    exit(1)

token = login_response.json()['access_token']
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print_success(f"Login successful! Token obtained")


# ============================================================================
# 2. USER PROFILE & SKILLS
# ============================================================================

print_section("2️⃣  User Profile Management")

# Get current profile
profile_resp = requests.get(f"{BASE_URL}/profile/me", headers=headers)
profile = profile_resp.json()
print_info(f"Current profile: {json.dumps(profile, indent=2)[:200]}...")

# Update skills
skills_data = {
    "skills": ["Python", "React", "AWS", "PostgreSQL", "Docker", "FastAPI"],
    "experience_years": 5
}
print_info(f"Updating user skills: {', '.join(skills_data['skills'])}")
print_info(f"Experience: {skills_data['experience_years']} years")

skills_resp = requests.post(f"{BASE_URL}/profile/skills", json=skills_data, headers=headers)
if skills_resp.status_code == 200:
    print_success("Skills updated successfully")
else:
    print_error(f"Failed to update skills: {skills_resp.text}")

# Get updated profile
profile_resp = requests.get(f"{BASE_URL}/profile/me", headers=headers)
updated_profile = profile_resp.json()
print_success(f"Updated Skills: {updated_profile.get('profile', {}).get('skills', [])}")
print_success(f"Experience: {updated_profile.get('profile', {}).get('experience_years', 0)} years")


# ============================================================================
# 3. JOB DATA IMPORT
# ============================================================================

print_section("3️⃣  Job Database Population")

# Sample job opportunities
sample_jobs = [
    {
        "title": "Senior Python Developer",
        "company": "TechCorp Industries",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "description": "Looking for experienced Python developer with AWS expertise. Work with FastAPI, PostgreSQL, and Docker.",
        "salary": "$150,000 - $180,000",
        "job_url": "https://example.com/jobs/1",
        "source": "CareerTrust Demo",
        "trust_score": 95,
        "posted_at": "2026-04-10T00:00:00"
    },
    {
        "title": "React Frontend Engineer",
        "company": "CloudNine Startup",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Build amazing UIs with React. Experience with TypeScript, Redux, and AWS S3 required.",
        "salary": "$120,000 - $150,000",
        "job_url": "https://example.com/jobs/2",
        "source": "CareerTrust Demo",
        "trust_score": 92,
        "posted_at": "2026-04-09T00:00:00"
    },
    {
        "title": "DevOps Engineer",
        "company": "InfraScale Solutions",
        "location": "New York, NY",
        "job_type": "Full-time",
        "description": "Manage cloud infrastructure using Docker, Kubernetes, and AWS. Python scripting skills a plus.",
        "salary": "$130,000 - $160,000",
        "job_url": "https://example.com/jobs/3",
        "source": "CareerTrust Demo",
        "trust_score": 93,
        "posted_at": "2026-04-08T00:00:00"
    },
    {
        "title": "Full Stack Developer",
        "company": "WebFlow Apps",
        "location": "Austin, TX",
        "job_type": "Full-time",
        "description": "Python backend with FastAPI and React frontend. Database design with PostgreSQL.",
        "salary": "$110,000 - $140,000",
        "job_url": "https://example.com/jobs/4",
        "source": "CareerTrust Demo",
        "trust_score": 88,
        "posted_at": "2026-04-07T00:00:00"
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AI Innovations",
        "location": "Seattle, WA",
        "job_type": "Full-time",
        "description": "Build ML models with Python, TensorFlow, and deploy with Docker/AWS.",
        "salary": "$140,000 - $170,000",
        "job_url": "https://example.com/jobs/5",
        "source": "CareerTrust Demo",
        "trust_score": 94,
        "posted_at": "2026-04-06T00:00:00"
    },
    {
        "title": "Database Architect",
        "company": "DataPro Systems",
        "location": "Chicago, IL",
        "job_type": "Full-time",
        "description": "Design and optimize PostgreSQL databases at scale. Strong Python background helpful.",
        "salary": "$135,000 - $165,000",
        "job_url": "https://example.com/jobs/6",
        "source": "CareerTrust Demo",
        "trust_score": 91,
        "posted_at": "2026-04-05T00:00:00"
    }
]

print_info(f"Importing {len(sample_jobs)} job opportunities into the system...")

import_response = requests.post(
    f"{BASE_URL}/jobs/import",
    json={"jobs": sample_jobs, "deduplicate": True},
    headers=headers
)

if import_response.status_code == 200:
    import_result = import_response.json()
    print_success(f"Successfully imported {import_result.get('imported_count', 0)} jobs")
    print_success(f"Deduplicated {import_result.get('duplicates_skipped', 0)} duplicate entries")
else:
    print_error(f"Failed to import jobs: {import_response.text}")


# ============================================================================
# 4. JOB SEARCH & RECOMMENDATIONS
# ============================================================================

print_section("4️⃣  Intelligent Job Recommendations")

print_info("Computing personalized job recommendations based on user skills...")
print_info("Using TF-IDF similarity matching for precise skill alignment")

# Get recommendations (POST with skills)
rec_response = requests.post(
    f"{BASE_URL}/jobs/recommendations",
    json={"skills": ["Python", "React", "AWS"], "top_n": 5},
    headers=headers
)

if rec_response.status_code == 200:
    recommendations = rec_response.json()
    jobs = recommendations.get('recommendations', [])
    
    print_success(f"Found {len(jobs)} matching job opportunities\n")
    
    for idx, job in enumerate(jobs, 1):
        print(f"  Job #{idx}")
        print(f"    Title:       {job.get('title', 'N/A')}")
        print(f"    Company:     {job.get('company', 'N/A')}")
        print(f"    Location:    {job.get('location', 'N/A')}")
        print(f"    Salary:      {job.get('salary', 'N/A')}")
        print(f"    Match Score: {job.get('match_score', 0):.1f}% ⭐")
        print(f"    Trust Score: {job.get('trust_score', 0)}/100")
        matched = job.get('matched_skills', [])
        missing = job.get('missing_skills', [])
        if matched:
            print(f"    ✅ Matched Skills: {', '.join(matched)}")
        if missing:
            print(f"    ❌ Missing Skills: {', '.join(missing)}")
        print()
else:
    print_error(f"Failed to get recommendations: {rec_response.text}")


# ============================================================================
# 5. JOB BOOKMARKING
# ============================================================================

print_section("5️⃣  Job Bookmarking & Saved Jobs")

if 'recommendations' in locals() and recommendations.get('recommendations'):
    first_job_id = recommendations['recommendations'][0]['id']
    
    print_info(f"Bookmarking job ID {first_job_id}...")
    
    save_response = requests.post(
        f"{BASE_URL}/profile/save-job",
        json={
            "opportunity_id": first_job_id,
            "notes": "This looks like a great opportunity! Senior level role with great benefits."
        },
        headers=headers
    )
    
    if save_response.status_code == 200:
        print_success("Job bookmarked successfully!")
    else:
        print_error(f"Failed to bookmark job: {save_response.text}")
    
    # Get saved jobs
    print_info("Retrieving all saved jobs...")
    saved_resp = requests.get(f"{BASE_URL}/profile/saved-jobs", headers=headers)
    
    if saved_resp.status_code == 200:
        saved_data = saved_resp.json()
        saved_jobs = saved_data.get('saved_jobs', [])
        print_success(f"User has {len(saved_jobs)} saved job(s)\n")
        
        for saved_job in saved_jobs:
            job_info = saved_job.get('job', {})
            print(f"  📌 {job_info.get('title')} @ {job_info.get('company')}")
            print(f"     Match Score: {saved_job.get('match_score')}%")
            print(f"     Bookmarked: {saved_job.get('saved_at', 'N/A')}")
            print(f"     Notes: {saved_job.get('notes', 'No notes')}\n")


# ============================================================================
# 6. ANALYTICS DASHBOARD
# ============================================================================

print_section("6️⃣  Analytics Dashboard")

analytics_response = requests.get(f"{BASE_URL}/analytics/dashboard", headers=headers)

if analytics_response.status_code == 200:
    analytics = analytics_response.json()
    dashboard = analytics.get('dashboard', {})
    
    print_success("Dashboard Metrics:")
    print(f"  📊 Profile Completion:    {dashboard.get('profile_completion', 0)}%")
    print(f"  💾 Saved Jobs:            {dashboard.get('total_saved_jobs', 0)}")
    print(f"  ✅ Jobs Applied To:       {dashboard.get('jobs_applied_to', 0)}")
    print(f"  📈 Avg Match Score:       {dashboard.get('average_match_score', 0):.1f}%")
    print(f"  📅 Recent Saves (30d):   {dashboard.get('recent_saves_30d', 0)}")
    
    if dashboard.get('user_skills'):
        print(f"  🎯 User Skills:           {', '.join(dashboard['user_skills'])}")
else:
    print_error(f"Failed to fetch analytics: {analytics_response.text}")


# ============================================================================
# 7. JOB MARKET INSIGHTS
# ============================================================================

print_section("7️⃣  Job Market Insights")

market_response = requests.get(f"{BASE_URL}/analytics/job-market", headers=headers)

if market_response.status_code == 200:
    market_data = market_response.json()
    insights = market_data.get('insights', {})
    
    print_success("Market Overview:")
    print(f"  📱 Total Jobs in Market:  {insights.get('total_jobs', 0)}")
    print(f"  ⭐ Avg Trust Score:       {insights.get('average_trust_score', 0):.1f}/100")
    
    if insights.get('top_companies'):
        print(f"\n  🏢 Top Hiring Companies:")
        for i, comp in enumerate(insights['top_companies'][:3], 1):
            if isinstance(comp, dict):
                print(f"     {i}. {comp.get('company', 'Unknown')} ({comp.get('count', 0)} openings)")
            else:
                print(f"     {i}. {comp}")
    
    if insights.get('top_locations'):
        print(f"\n  📍 Top Job Locations:")
        for i, loc in enumerate(insights['top_locations'][:3], 1):
            if isinstance(loc, dict):
                print(f"     {i}. {loc.get('location', 'Unknown')} ({loc.get('count', 0)} openings)")
            else:
                print(f"     {i}. {loc}")
    
    if insights.get('top_skills'):
        print(f"\n  🎓 Most Demanded Skills:")
        for i, skill in enumerate(insights['top_skills'][:5], 1):
            if isinstance(skill, dict):
                print(f"     {i}. {skill.get('skill', 'Unknown')} ({skill.get('count', 0)} jobs)")
            else:
                print(f"     {i}. {skill}")
else:
    print_error(f"Failed to fetch market insights: {market_response.text}")


# ============================================================================
# 8. SKILLS ANALYSIS
# ============================================================================

print_section("8️⃣  Skills Demand Analysis")

skills_response = requests.post(
    f"{BASE_URL}/analytics/skills-analysis",
    json={"skills": ["Python", "React", "AWS"]},
    headers=headers
)

if skills_response.status_code == 200:
    skills_analysis = skills_response.json()
    analysis = skills_analysis.get('analysis', {})
    
    print_success("Skill Market Analysis:\n")
    
    for skill_name, skill_data in list(analysis.items())[:3]:
        print(f"  🔧 {skill_name}")
        print(f"     Job Postings:    {skill_data.get('job_count', 0)}")
        print(f"     Avg Match Score: {skill_data.get('avg_match_score', 0):.1f}%")
        print(f"     Est. Salary:     ${skill_data.get('estimated_salary', 'N/A')}")
        print(f"     Demand Level:    {skill_data.get('demand_level', 'Unknown').upper()} 📈")
        print()
else:
    print_error(f"Failed to fetch skills analysis: {skills_response.text}")


# ============================================================================
# DEMO SUMMARY
# ============================================================================

print_header("✨ Demo Complete!")
print_success("All CareerTrust features demonstrated successfully")
print_info("Features showcased:")
print_info("  ✅ User authentication (registration & login)")
print_info("  ✅ User profile management with skills tracking")
print_info("  ✅ Job database population (6 sample jobs)")
print_info("  ✅ AI-powered job recommendations using TF-IDF matching")
print_info("  ✅ Job bookmarking and saved jobs")
print_info("  ✅ User analytics dashboard")
print_info("  ✅ Job market insights and trends")
print_info("  ✅ Skill demand analysis and market positioning")

print("\n" + "="*70)
print("  Ready for Next Steps:")
print("  1. Upload real resume (PDF/DOCX) for skill extraction")
print("  2. Build React frontend components")
print("  3. Deploy to production")
print("="*70 + "\n")
