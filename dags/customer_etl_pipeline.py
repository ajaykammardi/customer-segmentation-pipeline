from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# Import your local ETL functions
from etl.extract import extract_customers, extract_purchases, join_data
from etl.transform import clean_data, feature_engineering, feature_normalization, customer_segmenation, aggregate_segment_metrics, aggregate_behavior_metrics, aggregate_store_summary, aggregate_purchase_trends
from etl.load import load_to_db

import pandas as pd
import requests

# Paths
CUSTOMER_CSV = "data/customers.csv"
PURCHASE_API_URL = "http://127.0.0.1:8000/purchase-history"
PURSCHASE_CSV = "data/purchases.csv"
JOINED_CSV = "data/joined_data.csv"

# DAG definition
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

dag = DAG(
    dag_id='customer_etl_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='ETL pipeline for customer segmentation and reporting'
)

# Task 1: Extract Customer CSV
def task_extract_customer():
    customers_df = extract_customers()
    customers_df.to_csv(CUSTOMER_CSV, index=False)

# Task 2: Extract Purchase via API with actual customer mobiles
def task_extract_purchases():
    customers_df = pd.read_csv(CUSTOMER_CSV)
    customers_df = customers_df.drop_duplicates(subset='mobile')
    customers_df = customers_df[customers_df['mobile'].astype(str).str.match(r"^\d{10,}$")]
    mobiles = customers_df["mobile"].astype(str).tolist()
    print(f"Sending {len(mobiles)} mobiles to API...")
    extract_purchases(mobiles).to_csv("data/purchases.csv", index=False)

# Task 3: Join Data
def task_join_data():
    customers_df = pd.read_csv(CUSTOMER_CSV)
    purchases_df = pd.read_csv(PURSCHASE_CSV)
    joined_df = join_data(customers_df, purchases_df)
    joined_df.to_csv(JOINED_CSV, index=False)

# Task 4: Transform and Save Reporting Data
def task_transform():
    df = pd.read_csv(JOINED_CSV)
    df = clean_data(df)
    features = feature_engineering(df)
    features, features_scaled = feature_normalization(features)
    segments = customer_segmenation(features_scaled)
    features_with_segments, segment_metrics = aggregate_segment_metrics(features, segments)
    behavior_df = aggregate_behavior_metrics(df)
    store_df = aggregate_store_summary(df)
    trends_df = aggregate_purchase_trends(df)

    features_with_segments.to_csv("data/customer_segments.csv", index=False)
    segment_metrics.to_csv("data/segment_metrics.csv", index=False)
    behavior_df.to_csv("data/customer_behavior_metrics.csv", index=False)
    store_df.to_csv("data/customer_store_summary.csv", index=False)
    trends_df.to_csv("data/customer_purchase_trends.csv", index=False)

# Task 5: Load to DB
def task_load():
    load_to_db()

# Define PythonOperators
extract_customer = PythonOperator(
    task_id='extract_customer',
    python_callable=task_extract_customer,
    dag=dag
)

extract_purchase = PythonOperator(
    task_id='extract_purchase',
    python_callable=task_extract_purchases,
    dag=dag
)

join = PythonOperator(
    task_id='join_data',
    python_callable=task_join_data,
    dag=dag
)

transform = PythonOperator(
    task_id='transform_data',
    python_callable=task_transform,
    dag=dag
)

load = PythonOperator(
    task_id='load_to_postgres',
    python_callable=task_load,
    dag=dag
)

# DAG task dependencies
extract_customer >> extract_purchase >> join >> transform >> load
