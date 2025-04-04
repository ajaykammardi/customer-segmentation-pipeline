import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import numpy as np

def clean_data(df):
    df = df.drop_duplicates()
    df['age'] = df['age'].fillna(df['age'].median())
    df['income'] = df['income'].fillna(df['income'].median())
    df['amount'] = df['amount'].fillna(0)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def feature_engineering(df):
    today = pd.to_datetime("today")
    agg = df.groupby('mobile').agg({
        'amount': ['sum', 'mean', 'max', 'min', 'count'],
        'date': ['max', 'min'],
        'age': 'first',
        'income': 'first',
        'gender': 'first'
    })
    agg.columns = ['clv', 'avg_purchase_amount', 'max_purchase_amount', 'min_purchase_amount',
                   'purchase_count', 'last_purchase', 'first_purchase', 'age', 'income', 'gender']
    agg['last_purchase_days_ago'] = (today - agg['last_purchase']).dt.days
    agg['purchase_frequency'] = agg['purchase_count'] / ((agg['last_purchase'] - agg['first_purchase']).dt.days / 30.0).replace(0, 1)
    return agg.reset_index()

def feature_normalization(df):
    scaler = StandardScaler()
    df['gender'] = LabelEncoder().fit_transform(df['gender'].astype(str))
    cols = ['age', 'income', 'clv', 'avg_purchase_amount', 'purchase_count', 'last_purchase_days_ago', 'purchase_frequency']
    return df, scaler.fit_transform(df[cols])

def customer_segmenation(scaled_data, n_clusters=4):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    return model.fit_predict(scaled_data)

def aggregate_segment_metrics(df, segments):
    df['segment'] = segments
    summary = df.groupby('segment').agg({
        'clv': 'mean',
        'age': 'mean',
        'income': 'mean',
        'segment': 'count'
    }).rename(columns={'segment': 'num_customers'}).reset_index()
    return df, summary

def aggregate_behavior_metrics(df):
    today = pd.to_datetime("today")
    behavior = df.groupby("mobile").agg({
        "amount": ['sum', 'mean', 'max', 'min', 'count'],
        "date": ['min', 'max']
    })
    behavior.columns = ['total_spent', 'avg_transaction_value', 'max_purchase_amount',
                        'min_purchase_amount', 'purchase_count', 'first_purchase', 'last_purchase']
    behavior['days_since_first_purchase'] = (today - behavior['first_purchase']).dt.days
    behavior['days_since_last_purchase'] = (today - behavior['last_purchase']).dt.days
    return behavior.reset_index()

def aggregate_store_summary(df):
    store_summary = df.groupby(["mobile", "store"]).agg({
        "amount": ['sum', 'count']
    }).reset_index()
    store_summary.columns = ["mobile", "store", "total_spent", "visit_count"]
    return store_summary

def aggregate_purchase_trends(df):
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    monthly = df.groupby(["mobile", "month"]).agg({
        "amount": "sum",
        "date": "count"
    }).reset_index()
    monthly.columns = ["mobile", "month", "total_spent", "num_purchases"]
    return monthly
