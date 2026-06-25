build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec web python manage.py migrate

seed:
	docker compose exec web python manage.py seed_data

test:
	docker compose exec web pytest

coverage:
	docker compose exec web pytest --cov

lint:
	docker compose exec web ruff check .

format:
	docker compose exec web black .