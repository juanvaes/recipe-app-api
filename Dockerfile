FROM python:3.9-slim
LABEL manteiner="juanvaes22@gmail.com"

ARG DEV=false

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Tells Python to direct output to the console
ENV PYTHONBUFFERED 1

# Poetry
ENV POETRY_VERSION=1.1.8
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"
COPY . /recipe-app-api
WORKDIR /recipe-app-api

RUN if [ "$DEV" = "true" ] ; then \
        echo "installing dev dependencies..." && poetry install; \
    else \
        echo "installing prod dependencies..." && poetry install --no-dev; \
    fi
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user
EXPOSE 8000
USER django-user