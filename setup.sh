#!/bin/sh

# Update the package list
# sudo apt-get update

# Install xvfb (X virtual framebuffer)
# sudo apt-get install -y xvfb

echo "🚀 Setting up development environment..."

# Initialize database (check connection + create tables)
echo "📊 Initializing database..."
python init_db.py

# Seed test data
echo "🌱 Seeding test data..."
python test_data.py

# Echo the Flask run command
echo ""
echo "✅ Setup complete! Run the following command to start the app:"
flask --debug run --host=0.0.0.0 --port=5000
