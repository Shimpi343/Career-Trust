-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    skills JSON,
    interests JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Opportunities Table
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    job_type VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    salary VARCHAR(100),
    requirements TEXT,
    deadline TIMESTAMP,
    trust_score FLOAT DEFAULT 100,
    source VARCHAR(100),
    url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Applications Table
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    opportunity_id INTEGER NOT NULL REFERENCES opportunities(id),
    status VARCHAR(50),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_at TIMESTAMP
);

-- Scam Reports Table
CREATE TABLE scam_reports (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id),
    text_content TEXT,
    scam_score FLOAT,
    is_flagged BOOLEAN DEFAULT FALSE,
    suspicious_keywords JSON,
    analysis_result JSON,
    reported_by_user INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices for performance
CREATE INDEX idx_opportunities_job_type ON opportunities(job_type);
CREATE INDEX idx_opportunities_source ON opportunities(source);
CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_opportunity_id ON applications(opportunity_id);
CREATE INDEX idx_scam_reports_opportunity_id ON scam_reports(opportunity_id);
