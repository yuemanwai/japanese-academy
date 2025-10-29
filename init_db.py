#!/usr/bin/env python3
"""
Database connection check and initialization script.
Used in boot.sh to:
1. Wait for database to be ready
2. Create missing tables
"""
from app import db, app
import sys

try:
    with app.app_context():
        # Try to connect and execute a simple query
        db.engine.connect()
        print("✅ Database connection successful")
        
        # Create all tables if they don't exist
        db.create_all()
        print("✅ Database tables ready")
        
        sys.exit(0)
except Exception as e:
    print(f"❌ Database connection/initialization failed: {e}")
    sys.exit(1)
