#!/bin/sh
# This script is used to boot a Docker container

# 唔洗再 wait DB，因為 ArgoCD Sync Wave 確保左
# Job 跑完 (Table + Data 都 Ready) 先會 Deploy 呢個 Pod
echo "🎉 Starting Gunicorn..."
exec gunicorn app:app -b 0.0.0.0:5000 \
    --workers 1 \
    --threads 4 \
    --timeout 60 \
    --graceful-timeout 25 \
    --log-level info \
    --access-logfile - \
    --error-logfile - 
