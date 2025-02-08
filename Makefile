run:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf backend.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-geocity-api postgres:15

migrate:
	source ./venv/bin/activate && alembic upgrade head
