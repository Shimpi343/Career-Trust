#!/usr/bin/env python3
"""
Generate secure random values for Render environment variables.
Run this locally before setting up Render environment variables.

Usage:
    python generate_secrets.py
"""

import secrets
import sys

def generate_secrets():
    """Generate all required secret keys."""
    
    print("=" * 60)
    print("CareerTrust - Secure Secrets Generator")
    print("=" * 60)
    print()
    
    # Generate SECRET_KEY
    secret_key = secrets.token_urlsafe(32)
    print("1. SECRET_KEY (Flask session secret)")
    print(f"   Value: {secret_key}")
    print()
    
    # Generate JWT_SECRET_KEY
    jwt_secret = secrets.token_urlsafe(32)
    print("2. JWT_SECRET_KEY (JWT token secret)")
    print(f"   Value: {jwt_secret}")
    print()
    
    # Generate random password for local testing (optional)
    test_password = secrets.token_urlsafe(16)
    print("3. Random password (for local testing, optional)")
    print(f"   Value: {test_password}")
    print()
    
    print("=" * 60)
    print("INSTRUCTIONS:")
    print("=" * 60)
    print()
    print("✓ Step 1: Copy SECRET_KEY above")
    print("  - Go to Render dashboard → Environment")
    print("  - Add variable: Key=SECRET_KEY, Value=[paste above]")
    print()
    print("✓ Step 2: Copy JWT_SECRET_KEY above")
    print("  - Add variable: Key=JWT_SECRET_KEY, Value=[paste above]")
    print()
    print("✓ Step 3: Get Gmail App Password")
    print("  - Go to https://myaccount.google.com/apppasswords")
    print("  - Generate password for 'Mail' and 'Windows Computer'")
    print("  - Copy the 16-character password")
    print("  - Add variable: Key=SMTP_PASSWORD, Value=[paste gmail password]")
    print()
    print("=" * 60)
    print("Then add remaining variables (SMTP_HOST, etc.) from guide")
    print("=" * 60)

if __name__ == "__main__":
    try:
        generate_secrets()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
