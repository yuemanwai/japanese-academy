# 使用 Alpine 基礎映像檔
FROM python:3.11-alpine

# 在一個 RUN 區塊中安裝所有系統級套件並清理暫存
# 這樣能減少映像檔層數，並保持映像檔精簡
# 這裡將 apk update 與安裝指令合併，並在最後清理暫存
RUN apk update && \
    apk add --no-cache xvfb postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    rm -rf /var/cache/apk/*

# 建立使用者 jp 並設定工作目錄
RUN adduser -D jp
WORKDIR /home/jp

# 複製並安裝 Python 依賴
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk del .build-deps

# 複製所有應用程式檔案，並將所有權設定給 jp
COPY --chown=jp:jp ./app ./app
COPY --chown=jp:jp ./migrations ./migrations
COPY --chown=jp:jp ./chromedriver-linux64 ./chromedriver-linux64
COPY --chown=jp:jp ./config.py ./config.py
COPY --chown=jp:jp ./jp-academy.py ./run.py ./boot.sh ./test_data.py ./

# 授予 boot.sh 執行權限
RUN chmod +x boot.sh

# 設定環境變數
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# 切換到非 root 用戶，以確保容器安全
USER jp

# 暴露應用程式使用的 port
EXPOSE 5000

# 設定容器啟動時的入口點
ENTRYPOINT ["./boot.sh"]