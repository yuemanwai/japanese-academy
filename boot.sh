#!/bin/sh
# this script is used to boot a Docker container
apt-get update
apt-get install -y xvfb

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
python test_data.py
exec gunicorn -b :80 --access-logfile - --error-logfile - app:app
