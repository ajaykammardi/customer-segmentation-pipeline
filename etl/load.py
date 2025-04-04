import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def get_engine():
    return create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

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
