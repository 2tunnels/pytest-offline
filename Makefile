test:
	poetry run pytest -vv

format:
	poetry run isort --profile=black .
	poetry run black .
