.PHONY: install generate extract transform load test run-all docker-up docker-down

install:
	pip install -r requirements.txt

generate:
	python data/generate_customers.py

extract:
	python etl/extract.py

transform:
	python etl/transform.py

load:
	python etl/load.py

test:
	pytest tests/ || python -m unittest discover tests

run-all:
	make generate
	make extract
	make transform
	make load

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down
