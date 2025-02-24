
test:
	poetry run pytest tests/
	poetry run pylint ingest/ app/
	poetry run mypy ingest/