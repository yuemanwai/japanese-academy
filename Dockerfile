FROM python:3.11-alpine

RUN apk update && apk add xvfb
# RUN adduser -D jp-academy
WORKDIR /home/jp-academy

COPY requirements.txt requirements.txt
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN pip install Flask==2.2.2
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY chromedriver-linux64 chromedriver-linux64
COPY config.py config.py
COPY jp-academy.py run.py boot.sh test_data.py ./

RUN chmod +x boot.sh
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN chown -R jp-academy:jp-academy ./

# USER jp-academy
USER root

EXPOSE 80
ENTRYPOINT ["./boot.sh"]
