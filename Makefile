test:
	poetry run pytest -vv

format:
	poetry run isort --profile=black .
	poetry run black .

lint:
	poetry run isort --profile=black --check .
	poetry run black --check .
	poetry run flake8 --max-line-length=120 .
