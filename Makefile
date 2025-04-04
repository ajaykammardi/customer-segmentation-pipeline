.PHONY: install generate extract transform load test run-all docker-up docker-down

# 1. Install local Python dependencies (for local dev)
install:
\tpip install -r requirements.txt

# 2. Generate customer data
generate:
\tpython data/generate_customers_data.py

# 3. Run extraction (pull & merge data, e.g. from FastAPI)
extract:
\tpython etl/extract.py

# 4. Run transformation (clean, feature-engineer, cluster, aggregate)
transform:
\tpython etl/transform.py

# 5. Load final CSVs into Postgres
load:
\tpython etl/load.py

# 6. Basic test suite (pytest or custom tests)
test:
\tpytest tests/ || python -m unittest discover tests

# 7. Run entire ETL sequence (generate → extract → transform → load)
run-all:
\tmake generate
\tmake extract
\tmake transform
\tmake load

# 8. Docker commands
docker-up:
\tdocker-compose up --build -d

docker-down:
\tdocker-compose down
