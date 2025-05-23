ROOT := $(CURDIR)
SHELL := /bin/bash

env-config:
	python3 -m venv venv && \
	. venv/bin/activate && \
	
poetry-config:
	pip install poetry && \
	POETRY_VIRTUALENVS_CREATE=false poetry install

build-images:
	docker compose build

up-container:
	docker-compose up -d

apply-migrations:
	alembic upgrade head
