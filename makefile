ROOT := $(CURDIR)
SHELL := /bin/bash

env-config:
	python3 -m venv venv && \
	. venv/bin/activate && \
	
poetry-config:
	pip install poetry && \
	POETRY_VIRTUALENVS_CREATE=false poetry install

up-container:
	docker-compose up -d

apply-migrations:
	docker cp migrations/data/ hrf_universe_postgres:/tmp
	alembic upgrade head
