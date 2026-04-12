#!/usr/bin/env python
import traceback
import sys

try:
    print("Attempting to import Flask app...")
    from app import create_app, db
    print("Successfully imported create_app and db")
    
    print("Creating Flask app...")
    app = create_app()
    print("Flask app created successfully!")
    
    print("Creating database context...")
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    
    print("Running Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
