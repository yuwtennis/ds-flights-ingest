FROM python:3.11-slim

ENV APP_HOME=/app
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.8.3

WORKDIR $APP_HOME
COPY . ./

RUN apt update && apt -y install curl && apt clean
RUN curl -sSL https://install.python-poetry.org | python3 - && $POETRY_HOME/bin/poetry install

CMD exec $POETRY_HOME/bin/poetry run gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --chdir app/ main:app