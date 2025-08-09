#!/bin/sh

# Update the package list
sudo apt-get update

# Install xvfb (X virtual framebuffer)
sudo apt-get install -y xvfb

# Run the test_data.py script
python test_data.py

# Start the Flask application in debug mode, accessible from any host
flask --debug run --host=0.0.0.0 --port=5000