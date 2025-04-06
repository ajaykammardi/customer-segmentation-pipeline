# Customer Segmentation Pipeline

An end-to-end solution for **generating synthetic e-commerce customer data**, fetching purchase history from a **mock FastAPI** service, **transforming and clustering** customers using KMeans, and finally **loading** results into a **PostgreSQL** database.

---

## ⚙️ Requirements

- **Python 3.10** or higher. If you don't have Python installed, visit: [Python Downloads](https://www.python.org/downloads/)
- **Docker** & **Docker Compose** to run Postgres + FastAPI in containers:
  - [Docker Installation Guide](https://docs.docker.com/engine/install/)
  - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

---

## 📂 Project Structure

```
customer-segmentation-pipeline/
├── api/
│   └── purchase_history_api.py     # Mock FastAPI endpoint returning purchases
├── data/
│   ├── customers.csv               # Sample or generated customer data
│   └── generate_customers.py       # Script to generate synthetic CSV
├── db/
│   └── reporting_schema.sql        # Example table schema for reporting DB
├── docker/
│   ├── docker-compose.yml          # Docker config for Postgres + FastAPI
│   └── Dockerfile.api              # Docker build file for the FastAPI service
├── etl/
│   ├── extract.py                  # Extract from CSV + API, merge on 'mobile'
│   ├── transform.py                # Clean, feature engineer, KMeans cluster
│   └── load.py                     # Load final CSV outputs into PostgreSQL
├── tests/
│   └── test_etl.py                 # Basic test suite
├── dags/                           # (Optional) Airflow DAG for orchestration
│   └── customer_etl_pipeline.py
├── Makefile                        # Shortcut commands (generate, extract, transform, load, test)
├── requirements.txt                # Python dependencies
└── README.md                       # You're here!
```

---

## 📋 Pipeline Overview

1. **Data Generation**  
   - Creates `customers.csv` via `generate_customers.py`.
   - Contains random names, ages, incomes, mobiles, genders using the `faker` library.

2. **FastAPI Mock** (`purchase_history_api.py`)  
   - Returns random purchase data (date, amount, store) for each mobile number posted.
   - Allows integrating a dynamic data source during extraction.

3. **ETL Scripts**  
   - **Extract**:  
     - Reads `customers.csv`, calls FastAPI to get purchases per `mobile`, merges them into `joined_data.csv`.
   - **Transform**:  
     - Cleans missing values, standardizes dates, and handles numeric outliers.  
     - Computes features like Customer Lifetime Value (CLV), average purchase amount, purchase frequency, etc.  
     - Applies **KMeans** clustering (currently uses 3 or 4 clusters, no detailed cluster analysis or PCA steps).  
     - Outputs final **CSV** files, e.g. `customer_segments.csv`, `segment_metrics.csv`, etc. (These could be Parquet instead for larger datasets.)
   - **Load**:  
     - Connects to PostgreSQL (hosted by Docker) and writes final CSVs into tables like `customer_segments`, `segment_metrics`, `customer_behavior_metrics`, `customer_store_summary`, `customer_purchase_trends`.

4. **Reporting DB Schema**  
   Below is a sample schema (found in `db/reporting_schema.sql` or implicitly created via `to_sql`):
   ```
   CREATE TABLE IF NOT EXISTS customer_segments (
       mobile TEXT PRIMARY KEY,
       age INT,
       income FLOAT,
       gender TEXT,
       clv FLOAT,
       avg_purchase_amount FLOAT,
       purchase_count INT,
       last_purchase_days_ago INT,
       purchase_frequency FLOAT,
       segment INT
   );

   CREATE TABLE IF NOT EXISTS segment_metrics (
       segment INT PRIMARY KEY,
       clv FLOAT,
       age FLOAT,
       income FLOAT,
       num_customers INT
   );

   ... (etc. for behavior_metrics, store_summary, purchase_trends)
   ```

### Report Tables Summaries

- **customer_segments**  
  Per-customer records with demographic info (age, income, gender), computed features (CLV, purchase frequency), and assigned cluster segment.

- **segment_metrics**  
  Aggregated stats at the segment level (average CLV, average age, total customers, etc.).

- **customer_behavior_metrics**  
  Detailed purchase behavior per customer: total spent, average transaction value, first/last purchase date, etc.

- **customer_store_summary**  
  Spending summaries per (customer, store) pair with total spent, visit counts.

- **customer_purchase_trends**  
  Time-based monthly aggregates of spend and purchase counts per customer.

---

## Testing
- Basic test file in `tests/test_etl.py` checks data existence and quick logic validation.

## Optional Airflow DAG
- Found in `dags/customer_etl_pipeline.py`.
- Schedules or orchestrates the steps: generate → extract → transform → load.
- Useful for production scheduling or advanced monitoring.

---

## ⚙️ Assumptions & Simplifications

1. **KMeans Clusters**  
   - Hard-coded to **3 or 4** clusters; no advanced hyperparameter tuning or elbow plots. Deeper cluster analysis (e.g., PCA, silhouette scores) can be added if needed.
2. **Data Size**  
   - Uses **pandas**, suitable for small to medium data sets. For truly large data, consider **Polars** or **Apache Spark**.
3. **Data Generation**  
   - Simple random approach using `faker`. Real production might use real data or more domain-specific patterns.
4. **Data Quality**  
   - Minimal validations (imputation, removing missing `mobile`) — no deep business rules.
5. **Environment**  
   - Project is run via **Makefile** commands for simplicity.  
   - Docker Compose config assumes `db` service name for Postgres. If running locally (outside Docker), set `DB_HOST=localhost`.
6. **ETL**  
   - No orchestrator used by default, but a sample **Airflow** DAG is provided.
7. **Dockerizable ETL**  
   - The entire ETL (extract.py, transform.py, load.py) can also be wrapped in a Dockerfile and run as a container if desired.

---

## 🚀 Setup & Usage

### 1. **Install Python 3.10** (Local)

If you don’t have Python 3.10+, download it from [Python.org](https://www.python.org/downloads/) or use pyenv.

```bash
pip install -r requirements.txt


5. **Testing**  
   - Basic test file in `tests/test_etl.py` checks data existence and quick logic validation.

6. **Optional Airflow DAG**  
   - Found in `dags/customer_etl_pipeline.py`.  
   - Schedules or orchestrates the steps: generate → extract → transform → load.  
   - Useful for production scheduling or advanced monitoring.

---

## ⚙️ Assumptions & Simplifications

1. **KMeans Clusters**  
   - Hard-coded to **3 or 4** clusters; no advanced hyperparameter tuning or elbow plots. Deeper cluster analysis (e.g., PCA, silhouette scores) can be added if needed.
2. **Data Size**  
   - Uses **pandas**, suitable for small to medium data sets. For truly large data, consider **Polars** or **Apache Spark**.
3. **Data Generation**  
   - Simple random approach using `faker`. Real production might use real data or more domain-specific patterns.
4. **Data Quality**  
   - Minimal validations (imputation, removing missing `mobile`) — no deep business rules.
5. **Environment**  
   - Project is run via **Makefile** commands for simplicity.  
   - Docker Compose config assumes `db` service name for Postgres. If running locally (outside Docker), set `DB_HOST=localhost`.
6. **ETL**  
   - No orchestrator used by default, but a sample **Airflow** DAG is provided.
7. **Dockerizable ETL**  
   - The entire ETL (extract.py, transform.py, load.py) can also be wrapped in a Dockerfile and run as a container if desired.

---

## 🚀 Setup & Usage

### 1. **Install Python 3.10** (Local)

If you don’t have Python 3.10+, download it from [Python.org](https://www.python.org/downloads/) or use pyenv.

```bash
pip install -r requirements.txt
```
*(Or just `make install` if you have Make installed.)*

### 2. **Docker Compose** (Postgres + FastAPI)

Make sure you have Docker & Docker Compose installed:
- [Install Docker Engine](https://docs.docker.com/engine/install/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

From the `docker/` folder:
```bash
docker-compose up --build -d
```
- Postgres on port 5432
- FastAPI on port 8000

*(Adjust if you have separate Dockerfiles or combine them into one compose file.)*

### 3. **Make Commands**

From the project root (`customer-segmentation-pipeline/`):

```bash
# 3a. Start Docker if not started already
make docker-up

# 3b. Generate synthetic customer data
make generate

# 3c. Extract CSV + API data
make extract

# 3d. Transform: clean, engineer features, cluster
make transform

# 3e. Load results into Postgres
make load

# 3f. Run the entire pipeline at once
make run-all

# 3g. Test
make test
```

### 4. **Access the DB**
If using Docker, connect via:
```
psql -h localhost -U postgres -d customer_reporting
```
*(Replace credentials if needed.)*

---

## 🏗 Future Enhancements

1. **Cluster Optimization**  
   - Use the **elbow method** or **silhouette scores** or PCA to pick the ideal number of clusters.
2. **Scale & Performance**  
   - Switch from **pandas** to **Polars** or **Spark** for large datasets.
3. **File Formats**  
   - Currently, final & intermediate outputs are CSV files; consider **Parquet** for efficiency & compression at larger scale.
4. **Airflow**  
   - Deploy the **Airflow** DAG in `dags/` for production scheduling and monitoring.
5. **Advanced Data Quality**  
   - Integrate **Great Expectations** or **pandera** to validate schemas and handle missing or malformed data systematically.
6. **CI/CD**  
   - Add a GitHub Actions or GitLab pipeline for automated testing, linting, and container building.
7. **Analytics**  
   - Expand with dashboards (e.g., Metabase, Redash, or Grafana) against the final Postgres tables for real-time insights.

---
