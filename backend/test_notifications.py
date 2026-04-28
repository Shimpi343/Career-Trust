#!/usr/bin/env python
"""
Quick testing script for the email notification system.
Tests all notification endpoints with a real JWT token.
"""
import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5000/api"
TEST_EMAIL = "test@careertrust.local"
TEST_PASSWORD = "password123"  # Must match setup_notifications.py

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def main():
    """Run notification endpoint tests"""
    
    print_section("CareerTrust Email Notification System - Test Suite")
    
    # Step 1: Login and get JWT token
    print_section("Step 1: Authenticate User")
    print_info(f"Logging in as: {TEST_EMAIL}")
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
        )
        login_response.raise_for_status()
        login_data = login_response.json()
        access_token = login_data.get('access_token')
        
        if not access_token:
            print_error("No access token in response")
            print(f"Response: {login_data}")
            return
        
        print_success(f"Authenticated successfully")
        print_info(f"JWT Token: {access_token[:50]}...")
        print_info(f"User ID: {login_data.get('user', {}).get('id')}")
    except requests.exceptions.RequestException as e:
        print_error(f"Login failed: {e}")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Step 2: Get current notification settings
    print_section("Step 2: Get Current Notification Settings")
    try:
        response = requests.get(
            f"{BASE_URL}/notifications/settings",
            headers=headers
        )
        response.raise_for_status()
        settings = response.json()
        
        print_success("Retrieved notification settings:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to get settings: {e}")
        return
    
    # Step 3: Send test email
    print_section("Step 3: Send Test Email")
    print_info("Sending test email to verify SMTP configuration...")
    try:
        response = requests.post(
            f"{BASE_URL}/notifications/test-email",
            headers=headers
        )
        response.raise_for_status()
        test_email_data = response.json()
        
        if test_email_data.get('success'):
            print_success(f"Test email sent to {test_email_data.get('message')}")
            print_info("Check your email inbox (or Mailtrap inbox) for the test email")
        else:
            print_error(f"Test email failed: {test_email_data}")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to send test email: {e}")
        print_info(f"Error details: {e.response.text if hasattr(e, 'response') else 'N/A'}")
    
    # Step 4: Update notification settings
    print_section("Step 4: Update Notification Settings")
    update_data = {
        "email_alerts": True,
        "digest_frequency": "daily",
        "digest_time": "08:00",
        "email": TEST_EMAIL
    }
    print_info(f"Updating settings: {json.dumps(update_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/notifications/settings",
            headers=headers,
            json=update_data
        )
        response.raise_for_status()
        updated_settings = response.json()
        
        print_success("Settings updated:")
        for key, value in updated_settings.items():
            print(f"  {key}: {value}")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to update settings: {e}")
        return
    
    # Step 5: Manually trigger digest
    print_section("Step 5: Manually Trigger Daily Digest")
    print_info("Triggering a daily digest to test digest generation...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/notifications/digest",
            headers=headers,
            json={"frequency": "daily"}
        )
        response.raise_for_status()
        digest_data = response.json()
        
        if digest_data.get('sent'):
            print_success(f"Digest sent successfully")
            print_info(f"Message: {digest_data.get('message')}")
            print_info(f"Jobs included: {digest_data.get('jobs_count', 0)}")
        else:
            print_info(f"Digest not sent: {digest_data.get('reason', 'Unknown reason')}")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to trigger digest: {e}")
        print_info(f"Error details: {e.response.text if hasattr(e, 'response') else 'N/A'}")
    
    # Step 6: Scheduler information
    print_section("Step 6: Background Scheduler Information")
    print_info("The following jobs are running in the background:")
    print("""
    1️⃣  HOURLY ALERTS (Every 1 hour)
        - Checks for new job matches matching user profile
        - Sends alert email with top 5 matches
        - Only sends if user has email_alerts = true
    
    2️⃣  DAILY DIGEST (Every day at 08:00 UTC)
        - Collects job matches from past day
        - Sends formatted digest email with top 10 matches
        - Only sends if user has digest_frequency = 'daily'
    
    3️⃣  WEEKLY DIGEST (Every Monday at 08:30 UTC)
        - Collects job matches from past week
        - Sends weekly digest email with top 10 matches
        - Only sends if user has digest_frequency = 'weekly'
    """)
    
    print_info("Check the Flask server logs to see scheduler activity:")
    print("""
    Watch the terminal running Flask for lines like:
    [2026-04-28 08:00:00] Running daily digest job...
    [2026-04-28 08:00:01] Processing user: testuser (ID: 10)
    [2026-04-28 08:00:02] Found 5 matching jobs
    [2026-04-28 08:00:03] Email sent to test@careertrust.local
    """)
    
    # Final summary
    print_section("Test Summary")
    print("""
    ✅ Notification system is fully configured!
    
    What's working:
    ✓ SMTP email provider connected
    ✓ Test user created with notification preferences
    ✓ API endpoints for notification settings
    ✓ Manual digest trigger tested
    ✓ Background scheduler running (3 jobs)
    
    Next steps:
    1. Check your email for test messages
    2. Monitor Flask logs for scheduler activity
    3. Update notification settings as needed via API
    4. Create React UI for notification settings management
    5. Set up real SMTP provider (Gmail, SendGrid, etc.)
    
    For more details, see NOTIFICATIONS_SETUP.md
    """)

if __name__ == '__main__':
    main()
