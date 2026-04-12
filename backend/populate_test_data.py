"""
Script to populate CareerTrust database with sample data
Run this after starting the backend: python populate_test_data.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

# Sample test data
USERS = [
    {
        "email": "student1@example.com",
        "username": "student1",
        "password": "password123"
    },
    {
        "email": "student2@example.com",
        "username": "student2",
        "password": "password123"
    }
]

OPPORTUNITIES = [
    {
        "title": "Junior Web Developer",
        "company": "Tech Startup Inc",
        "description": "We are looking for a talented junior web developer with 1-2 years of experience. You will work on front-end and back-end development using React and Python Flask.",
        "job_type": "job",
        "location": "San Francisco, CA",
        "salary": "$60,000 - $75,000/year",
        "requirements": "HTML, CSS, JavaScript, React, Python",
        "source": "LinkedIn"
    },
    {
        "title": "Summer Internship - Data Science",
        "company": "DataCorp Solutions",
        "description": "Join our data science team for a 12-week summer internship. Work on real-world ML projects and learn from experienced practitioners.",
        "job_type": "internship",
        "location": "New York, NY",
        "salary": "$20/hour",
        "requirements": "Python, Statistics, Machine Learning basics",
        "source": "Indeed"
    },
    {
        "title": "Frontend Engineer (Entry Level)",
        "company": "Creative Web Studios",
        "description": "Looking for passionate frontend developers to join our creative team. We build beautiful, responsive web applications for Fortune 500 companies.",
        "job_type": "job",
        "location": "Remote",
        "salary": "$55,000 - $70,000/year",
        "requirements": "React, Vue or Angular, CSS, JavaScript",
        "source": "GitHub Jobs"
    },
    {
        "title": "Summer Hackathon 2024",
        "company": "Tech Innovation Hub",
        "description": "Annual 48-hour hackathon. Build innovative projects, network with peers, and win exciting prizes. All skill levels welcome!",
        "job_type": "hackathon",
        "location": "Boston, MA",
        "salary": "Prizes: $5,000 total",
        "requirements": "Any programming language",
        "source": "Hackathon.com"
    },
    {
        "title": "Backend Developer - Cloud Services",
        "company": "CloudTech Enterprises",
        "description": "Develop scalable backend services using Python and AWS. We're looking for developers who are passionate about building robust systems.",
        "job_type": "job",
        "location": "Austin, TX",
        "salary": "$70,000 - $85,000/year",
        "requirements": "Python, AWS, Docker, SQL",
        "source": "LinkedIn"
    },
    {
        "title": "Full Stack Internship",
        "company": "StartupXYZ",
        "description": "3-month internship working on full stack development. Great opportunity to learn and contribute to a growing startup.",
        "job_type": "internship",
        "location": "Seattle, WA",
        "salary": "$18/hour",
        "requirements": "JavaScript, React, Node.js, MongoDB",
        "source": "LinkedIn"
    },
    {
        "title": "Quality Assurance Engineer",
        "company": "SoftTech Solutions",
        "description": "Join our QA team to ensure software quality. Experience with automated testing and Python required.",
        "job_type": "job",
        "location": "Chicago, IL",
        "salary": "$50,000 - $65,000/year",
        "requirements": "Python, Selenium, Test Automation",
        "source": "Indeed"
    },
    {
        "title": "DevOps Internship - Cloud Infrastructure",
        "company": "InfraCloud Inc",
        "description": "12-week internship focused on cloud infrastructure and DevOps practices. Work with Kubernetes, Docker, and CI/CD pipelines.",
        "job_type": "internship",
        "location": "Remote",
        "salary": "$17/hour",
        "requirements": "Linux, Docker, Basic cloud knowledge",
        "source": "GitHub Jobs"
    }
]

def register_user(email, username, password):
    """Register a new user"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": email,
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print(f"✓ User registered: {email}")
        return response.json()
    elif response.status_code == 409:
        print(f"ℹ User already exists: {email}")
        return None
    else:
        print(f"✗ Failed to register {email}: {response.json()}")
        return None

def login_user(email, password):
    """Login and get JWT token"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✓ User logged in: {email}")
        return token
    else:
        print(f"✗ Failed to login {email}: {response.json()}")
        return None

def create_opportunity(token, opportunity):
    """Create a new opportunity"""
    url = f"{BASE_URL}/opportunities"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=opportunity, headers=headers)
    if response.status_code == 201:
        print(f"✓ Opportunity created: {opportunity['title']}")
        return response.json()
    else:
        print(f"✗ Failed to create opportunity: {response.json()}")
        return None

def main():
    print("\n" + "="*60)
    print("CareerTrust - Test Data Population Script")
    print("="*60 + "\n")
    
    # Step 1: Register users
    print("Step 1: Registering/checking users...")
    print("-" * 60)
    for user_data in USERS:
        register_user(user_data["email"], user_data["username"], user_data["password"])
    
    # Step 2: Login first user and get token
    print("\nStep 2: Logging in user...")
    print("-" * 60)
    token = login_user(USERS[0]["email"], USERS[0]["password"])
    
    if not token:
        print("\n✗ Failed to login. Exiting.")
        return
    
    # Step 3: Create opportunities
    print("\nStep 3: Creating opportunities...")
    print("-" * 60)
    for opportunity in OPPORTUNITIES:
        create_opportunity(token, opportunity)
    
    print("\n" + "="*60)
    print("✓ Test data population complete!")
    print("="*60)
    print("\nYou can now:")
    print("1. Visit http://localhost:3000")
    print("2. Click 'Opportunities' to see all opportunities")
    print("3. Login with:")
    print(f"   Email: {USERS[0]['email']}")
    print(f"   Password: {USERS[0]['password']}")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to backend server!")
        print("Make sure the backend is running at http://localhost:5000")
        print("\nTo start the backend, open a terminal and run:")
        print("  cd backend")
        print("  .\\venv\\Scripts\\activate.bat")
        print("  python app.py")
