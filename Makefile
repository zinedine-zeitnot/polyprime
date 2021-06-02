format:
	poetry run isort . && poetry run black .

style:
	poetry run flake8 .

test:
	poetry run pytest --cov=.
