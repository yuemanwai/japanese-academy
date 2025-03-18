#!/bin/sh
# this script is used to boot a Docker container
sudo apt-get update
sudo apt-get install -y xvfb

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
python test_data.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - wikipedia:app
