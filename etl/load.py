import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def get_engine():
    # Use environment variables; fallback defaults can help debugging locally
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")          # 'db' matches service name in docker-compose
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "customer_reporting")

    url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(url)

def load_to_db():
    engine = get_engine()
    files_to_tables = {
        "data/customer_segments.csv": "customer_segments",
        "data/segment_metrics.csv": "segment_metrics",
        "data/customer_behavior_metrics.csv": "customer_behavior_metrics",
        "data/customer_store_summary.csv": "customer_store_summary",
        "data/customer_purchase_trends.csv": "customer_purchase_trends"
    }

    for file_path, table in files_to_tables.items():
        print(f"Loading {table}")
        pd.read_csv(file_path).to_sql(table, engine, if_exists="replace", index=False)

# Optional: standalone testable main
if __name__ == "__main__":
    load_to_db()