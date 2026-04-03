# 1) Lightweight uv Alpine base image.
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Faster startup with bytecode; use system Python.
ENV UV_COMPILE_BYTECODE=1
ENV UV_SYSTEM_PYTHON=1

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
RUN --mount=type=cache,target=/root/.cache/uv \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    uv pip install -r requirements.txt && \
    apk del .build-deps

# 4) Run as non-root user for security.
# Avoid running containers as root in production.
RUN adduser -D jp

# Copy files with non-root ownership.
COPY --chown=jp:jp ./app ./app
COPY --chown=jp:jp ./migrations ./migrations
# Keep chromedriver for compatibility/debug; not started by default.
COPY --chown=jp:jp ./chromedriver-linux64 ./chromedriver-linux64
COPY --chown=jp:jp ./config.py ./config.py
COPY --chown=jp:jp ./jp-academy.py ./run.py ./boot.sh ./test_data.py ./init_db.py ./

# Make entrypoint executable.
RUN chmod +x boot.sh

# Start container as non-root.
USER jp
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
