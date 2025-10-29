#!/bin/sh
# This script is used to boot a Docker container

echo "🚀 Starting application boot sequence..."

# Wait for database to be ready and create tables
echo "📊 Initializing database..."
while true; do
    python init_db.py
    if [[ "$?" == "0" ]]; then
        echo "✅ Database is ready"
        break
    fi
    echo "⚠️  Database not ready, retrying in 15 secs..."
    sleep 15
done

# Seed data
echo "🌱 Seeding data..."
python test_data.py

# Start the application
echo "🎉 Starting Gunicorn..."
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app
