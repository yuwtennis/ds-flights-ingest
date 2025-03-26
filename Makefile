
test:
	poetry run pytest tests/
	poetry run pylint ds_flights_ingest/ app/
	poetry run mypy ds_flights_ingest/ app/