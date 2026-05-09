# 1) Lightweight uv Alpine base image.
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Faster startup with bytecode; use system Python.
ENV UV_COMPILE_BYTECODE=1
ENV UV_SYSTEM_PYTHON=1
# OpenShift restricted-v2 runs with arbitrary UID; set HOME and XDG paths to writable dirs.
ENV HOME=/home/jp
ENV XDG_CACHE_HOME=/home/jp/var/cache
ENV XDG_CONFIG_HOME=/home/jp/var/config
ENV XDG_DATA_HOME=/home/jp/var/data
ENV TMPDIR=/home/jp/var/tmp

WORKDIR /home/jp

# 2) Install only required PostgreSQL runtime libs.
# Fewer packages = smaller image and lower attack surface.
RUN apk update && \
    apk upgrade --no-cache && \
    apk add --no-cache postgresql-libs zlib && \
    rm -rf /var/cache/apk/*

# 3) Install Python deps with cache for faster rebuilds.
# Remove build-only packages after install.
COPY requirements.txt .
RUN --mount=type=cache,target=/var/cache/uv \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python -m pip install --upgrade pip setuptools wheel && \
    uv pip install -r requirements.txt && \
    apk del .build-deps

# 4) Non-root user entry for libs expecting /etc/passwd.
# OpenShift will override UID at runtime; keep GID 0 for fsGroup alignment.
RUN adduser -D -u 1001 -G root jp && \
    mkdir -p /home/jp && \
    chown -R 1001:0 /home/jp

# Copy files with non-root ownership.
COPY --chown=1001:0 ./app ./app
COPY --chown=1001:0 ./migrations ./migrations
# Keep chromedriver for compatibility/debug; not started by default.
COPY --chown=1001:0 ./chromedriver-linux64 ./chromedriver-linux64
COPY --chown=1001:0 ./config.py ./config.py
COPY --chown=1001:0 ./jp-academy.py ./run.py ./boot.sh ./test_data.py ./init_db.py ./

# Make entrypoint executable.
RUN chmod +x boot.sh

# OpenShift: grant GID 0 write access to app writable paths only.
RUN mkdir -p /home/jp/var/cache /home/jp/var/config /home/jp/var/data /home/jp/var/tmp && \
    chgrp -R 0 /home/jp/var && \
    chmod -R g=u /home/jp/var && \
    chgrp -R 0 /home/jp/app/static/video /home/jp/app/static/image && \
    chmod -R g=u /home/jp/app/static/video /home/jp/app/static/image

# Start container as non-root (explicit UID:GID for restricted-v2).
USER 1001:0
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
