SHELL := bash
BACKEND = backend/moonshot/*.py backend/api/*.py
isort = isort $(BACKEND)
black = @black --target-version py38 $(BACKEND)

all: test


install-dev:
	pip install -r backend/requirements.txt
	npm --prefix ./frontend install ./frontend


test: install-dev lint
	python manage.py test


format:
	$(isort)
	$(black)

lint:
	flake8 $(BACKEND)
	$(isort) --check-only
	$(black) --check
	mypy $(BACKEND)

start:
	python backend/manage.py runserver &
	cd frontend && npm start
