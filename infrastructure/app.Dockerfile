FROM python:3.12-slim-bullseye


# && apk add gcc make git libc-dev binutils-gold
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      python3-dev \
      libffi-dev \
      libpq-dev \
      gettext \
      git \
      curl \
 && pip install --upgrade pip setuptools wheel \
 && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y make git libc-dev binutils-gold gcc g++


ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_INSTALL_ARGS="--no-root --only main" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME="/etc/poetry"
    
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry lock --regenerate
RUN poetry install $POETRY_INSTALL_ARGS

COPY . .

EXPOSE 8000


# RUN alembic upgrade head
ENTRYPOINT python3 entrypoint.py