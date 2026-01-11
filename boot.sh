#!/bin/sh
# This script is used to boot a Docker container

# echo "🚀 Starting application boot sequence..."

# # Wait for database to be ready and create tables
# echo "📊 Initializing database..."
# while true; do
#     python init_db.py
#     if [[ "$?" == "0" ]]; then
#         echo "✅ Database is ready"
#         break
#     fi
#     echo "⚠️  Database not ready, retrying in 10 secs..."
#     sleep 10
# done

# # Seed data
# echo "🌱 Seeding data..."
# python test_data.py

# 唔再做 python init_db.py，直接開波
# Start the application
echo "🎉 Starting Gunicorn..."
exec gunicorn app:app -b 0.0.0.0:5000 \
    --workers 1 \
    --threads 4 \
    --timeout 60 \
    --graceful-timeout 25 \
    --log-level info \
    --access-logfile - \
    --error-logfile - 
