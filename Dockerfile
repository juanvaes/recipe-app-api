# Builder stage
FROM python:3.9-slim AS builder
LABEL manteiner="juanvaes22@gmail.com"
ARG DEV=false

# libpq-dev is a very light and minimal package used to interact with a postgresql db
# gcc a kind of C compiler to install psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Creates virtualenv
RUN python -m venv /opt/venv
# Activates virtualenvironment
ENV PATH="/opt/venv/bin:$PATH"


# Poetry
# ------
ENV POETRY_VERSION=1.3.2
RUN pip install poetry==${POETRY_VERSION}
COPY poetry.lock pyproject.toml .

RUN if [ "$DEV" = "true" ] ; then \
        echo "installing dev dependencies..." \
        && poetry config virtualenvs.create false \
        && poetry install --no-interaction --no-ansi; \

    else \
        echo "installing prod dependencies..." \
        && poetry config virtualenvs.create false \
        && poetry install --no-dev --no-interaction --no-ansi; \
    fi

FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y libpq-dev

COPY --from=builder /opt/venv /opt/venv

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONBUFFERED 1

ENV PATH="/scripts:/opt/venv/bin:$PATH"

WORKDIR /usr/src/app

COPY config /usr/src/app/config
COPY bin /usr/src/app/bin
COPY manage.py /usr/src/app/
COPY poetry.lock /usr/src/app/
COPY pyproject.toml /usr/src/app/
COPY core /usr/src/app/core
COPY user /usr/src/app/user
COPY recipe /usr/src/app/recipe

RUN mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chmod -R 755 /vol

#RUN adduser \
#    --disabled-password \
#    --no-create-home \
#    django-user
EXPOSE 8000
#USER django-user
CMD ["run.sh"]