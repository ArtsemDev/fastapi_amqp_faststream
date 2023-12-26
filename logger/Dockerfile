FROM python:3.11.7-alpine3.18

ARG APP_NAME=logger
ARG APP_PATH=/opt/$APP_NAME
ARG UNAME=www
ARG UID=1000

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR $APP_PATH
COPY ./logger $APP_PATH
RUN pip install --no-cache-dir --upgrade -r $APP_PATH/requirements.txt && \
    adduser -u $UID -s /bin/bash -D -S $UNAME
USER $UNAME