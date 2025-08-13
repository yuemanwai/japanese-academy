#!/bin/sh
# this script is used to boot a Docker container
# apt-get update
# apt-get install -y xvfb
# apk update && apk add xvfb
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 15 secs...
    sleep 15
done
python test_data.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app
