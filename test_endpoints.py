#!/usr/bin/env python
import requests
import json

print("\n=== Testing All Endpoints ===\n")

# Get token
print("1. Testing Login...")
login_resp = requests.post('http://localhost:5000/api/auth/login', json={'email': 'full@test.com', 'password': 'TestPass123'})
if login_resp.status_code != 200:
    print(f"   ✗ Login failed: {login_resp.text}")
    exit(1)
token = login_resp.json()['access_token']
print("   ✓ Login successful")

headers = {'Authorization': f'Bearer {token}'}

# Test profile endpoint
print("\n2. Testing Profile Endpoint...")
profile = requests.get('http://localhost:5000/api/profile/me', headers=headers)
if profile.status_code == 200:
    prof_data = profile.json()
    print(f"   ✓ Profile retrieved")
    print(f"     - Skills: {prof_data.get('skills', [])}")
    print(f"     - Experience: {prof_data.get('experience_years', 0)} years")
else:
    print(f"   ✗ Profile failed: {profile.text}")

# Test recommendations endpoint (POST with skills)
print("\n3. Testing Job Recommendations...")
recs = requests.post('http://localhost:5000/api/jobs/recommendations',
                     headers=headers,
                     json={'skills': ['python', 'react']})
if recs.status_code == 200:
    data = recs.json()
    print(f"   ✓ Recommendations retrieved")
    recs_list = data.get('recommendations', data.get('jobs', []))
    print(f"     - Total jobs: {len(recs_list)}")
    if recs_list:
        job = recs_list[0]
        print(f"     - Sample: {job['title']} @ {job['company']} (match: {job.get('match_score', 'N/A')}%)")
else:
    print(f"   ✗ Recommendations failed: {recs.text}")

# Test analytics dashboard
print("\n4. Testing Analytics Dashboard...")
analytics = requests.get('http://localhost:5000/api/analytics/dashboard', headers=headers)
if analytics.status_code == 200:
    dash = analytics.json()
    dashboard_data = dash.get('dashboard', dash)
    print(f"   ✓ Analytics dashboard retrieved")
    print(f"     - Profile completion: {dashboard_data.get('profile_completion', 'N/A')}%")
    print(f"     - Saved jobs: {dashboard_data.get('total_saved_jobs', 0)}")
else:
    print(f"   ✗ Analytics failed: {analytics.text}")

# Test job market insights
print("\n5. Testing Job Market Insights...")
market = requests.get('http://localhost:5000/api/analytics/job-market', headers=headers)
if market.status_code == 200:
    mkt_data = market.json()
    insights = mkt_data.get('insights', mkt_data)
    print(f"   ✓ Market insights retrieved")
    print(f"     - Top skills: {len(insights.get('top_skills', []))} skills identified")
    print(f"     - Top companies: {len(insights.get('top_companies', []))} companies")
else:
    print(f"   ✗ Market insights failed: {market.text}")

# Test job search
print("\n6. Testing Job Search by Skills...")
search = requests.post('http://localhost:5000/api/jobs/search', 
                      headers=headers,
                      json={'skills': ['python', 'react']})
if search.status_code == 200:
    search_data = search.json()
    print(f"   ✓ Job search works")
    print(f"     - Found {len(search_data['jobs'])} matching jobs")
else:
    print(f"   ✗ Job search failed: {search.text}")

print("\n=== All Tests Complete ===\n")
