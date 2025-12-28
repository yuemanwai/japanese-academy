#!/bin/bash

# Update the package list
# apt-get update

# Install xvfb (X virtual framebuffer)
# apt-get install -y xvfb

echo "🚀 Setting up development environment..."

# Verify environment variables are available
if [ -z "$SQLALCHEMY_DATABASE_URI" ]; then
    echo "[ERROR] SQLALCHEMY_DATABASE_URI is not set!"
    exit 1
fi

echo "[INFO] Using database: $SQLALCHEMY_DATABASE_URI"
echo "[INFO] Flask environment: $FLASK_ENV"

# Initialize database (check connection + create tables)
echo "📊 Initializing database..."
python init_db.py || exit 1

# Seed test data
echo "🌱 Seeding test data..."
python test_data.py || exit 1

# Echo the Flask run command
echo ""
echo "✅ Setup complete! Run the following command to start the app:"
echo "SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@postgresdb:5432/postgres' FLASK_ENV='development' flask --debug run --host=0.0.0.0 --port=5000"
