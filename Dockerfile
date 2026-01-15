# 1. 使用 uv 官方 Alpine (最輕量)
FROM ghcr.io/astral-sh/uv:python3.13-alpine

ENV UV_COMPILE_BYTECODE=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /home/jp

# 2. 只安裝真正需要的 lib (Postgres)
# 移除了 xvfb, gcompat, libstdc++ -> 幫你省空間
RUN apk update && \
    apk add --no-cache postgresql-libs && \
    rm -rf /var/cache/apk/*

# 3. 依賴安裝 (Cache Mount 加速)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    uv pip install -r requirements.txt && \
    apk del .build-deps

# 4. 應用程式
RUN adduser -D jp

# 照樣 Copy 你的程式碼和 driver (保留證據)
COPY --chown=jp:jp ./app ./app
COPY --chown=jp:jp ./migrations ./migrations
# 這裡照樣 copy 進去，反正不跑不吃 RAM，但證明你有這個檔案
COPY --chown=jp:jp ./chromedriver-linux64 ./chromedriver-linux64 
COPY --chown=jp:jp ./config.py ./config.py
COPY --chown=jp:jp ./jp-academy.py ./run.py ./boot.sh ./test_data.py ./init_db.py ./

RUN chmod +x boot.sh

USER jp
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]