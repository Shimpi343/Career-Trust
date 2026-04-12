# CareerTrust Deployment Guide

## Environment Variables

Create `.env` file in backend directory:

```
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/careertrust_dev
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
```

## Database Setup

### PostgreSQL Installation (Windows)
1. Download from https://www.postgresql.org/download/windows/
2. Run installer
3. Create database: `createdb careertrust_dev`
4. Apply schema: `psql careertrust_dev < database/schema.sql`

### Database Verification
```bash
psql careertrust_dev
\dt  # List tables
\q   # Quit
```

## Backend Deployment

### Development
```bash
cd backend
python app.py
# Server runs on http://localhost:5000
```

### Production
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Frontend Deployment

### Development
```bash
cd frontend
npm start
# Application runs on http://localhost:3000
```

### Production Build
```bash
npm run build
# Creates optimized build in build/ directory

# Serve with production server
npm install -g serve
serve -s build -l 3000
```

## Docker Deployment (Optional)

Create `Dockerfile` in backend:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t careertrust-backend .
docker run -p 5000:5000 -e DATABASE_URL=... careertrust-backend
```

## File Paths (Windows)
- Python: `C:\Users\kumar\AppData\Local\Programs\Python`
- PostgreSQL: `C:\Program Files\PostgreSQL`
- Project: `C:\Users\kumar\Downloads\Career Trust`
