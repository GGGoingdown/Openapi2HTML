FROM python:3.9-slim as requirements-stage
WORKDIR /tmp
ARG ENVIRONMENT=PROD
RUN pip install --upgrade pip poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.9-slim as build-stage

WORKDIR /src
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Pyproject
COPY pyproject.toml .

# Main file
COPY ./src .
