#!/bin/sh
sudo apt-get update
sudo apt-get install -y xvfb
python test_data.py
flask --debug run --host=0.0.0.0