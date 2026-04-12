# Data migrations for CareerTrust

## Migration 001: Initial Schema
- Create users, opportunities, applications, scam_reports tables
- Create indices for performance

## Migration 002: Add Platform Integration
- Add platform_credentials table for OAuth integration
- Add data_source table to track different job platforms

## Process
1. Install Flask-Migrate: `pip install Flask-Migrate`
2. Initialize migrations: `flask db init`
3. Create migration: `flask db migrate`
4. Apply migration: `flask db upgrade`
