FROM python:3.10-alpine

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work directory
WORKDIR /usr/src/app

# Install psycopg dependencies
RUN apk update && apk --no-cache --update add \
    build-base \
    libpq-dev

# Install dependencies
RUN pip install --upgrade pip pipenv
COPY Pipfile* ./
RUN pipenv install --system --ignore-pipfile

COPY . .