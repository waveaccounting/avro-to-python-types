FROM python:3.9.9-bullseye

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
  git vim iputils-ping curl \
  && pip install "poetry>=1.1.11" \
  && poetry config experimental.new-installer false \
  && poetry config virtualenvs.create false \
  && poetry install --no-root


ENV PYTHONPATH=/app
WORKDIR /app
COPY ./ /app/
CMD poetry run pytest tests