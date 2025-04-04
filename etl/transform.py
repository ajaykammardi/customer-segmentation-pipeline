import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import numpy as np

INPUT_FILE = "data/joined_data.csv"
OUTPUT_SEGMENTS_FILE = "data/customer_segments.csv"
OUTPUT_METRICS_FILE = "data/segment_metrics.csv"
OUTPUT_CUSTOMER_BEHAVIOR_METRICS_FILE = "data/customer_behavior_metrics.csv"
OUTPUT_CUSTOMER_STORE_METRICS_FILE = "data/customer_store_summary.csv"
OUTPUT_PURCHASE_TRENDS_FILE = "data/customer_purchase_trends.csv"

def clean_data(df):
    df = df.drop_duplicates()
    df['age'] = df['age'].fillna(df['age'].median())
    df['income'] = df['income'].fillna(df['income'].median())
    df['amount'] = df['amount'].fillna(0)
    
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

    # Fill any rows that failed with a second parse (assuming those might be Y-M-D)
    mask_failed = df['date'].isna()
    df.loc[mask_failed, 'date'] = pd.to_datetime( df.loc[mask_failed, 'date'], format='%d-%m-%Y', errors='coerce')

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
    
    agg['days_since_last_purchase'] = (today - agg['last_purchase']).dt.days
    agg['purchase_frequency'] = agg['purchase_count'] / ((agg['last_purchase'] - agg['first_purchase']).dt.days / 30.0).replace(0, 1)

    agg['days_since_first_purchase'] = (today - agg['first_purchase']).dt.days
    
    print(len(agg))
    agg = agg.dropna()
    print(len(agg))
    
    return agg.reset_index()

def feature_normalization(df):
    scaler = StandardScaler()
    df['gender'] = LabelEncoder().fit_transform(df['gender'].astype(str))
    cols = ['age', 'income', 'clv', 'avg_purchase_amount', 'purchase_count', 'days_since_last_purchase', 'purchase_frequency']
    return df, scaler.fit_transform(df[cols])

def customer_segmenation(scaled_data, n_clusters=3):
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

def main():
    df = pd.read_csv(INPUT_FILE)
    df = clean_data(df)
    featured_df = feature_engineering(df)
    
    features, features_scaled = feature_normalization(featured_df)
    segments = customer_segmenation(features_scaled)

    features_with_segments, segment_metrics = aggregate_segment_metrics(features, segments)
    aggregate_behavior_metrics_df = aggregate_behavior_metrics(df)
    aggregate_store_summary_df = aggregate_store_summary(df)
    aggregate_purchase_trends_df = aggregate_purchase_trends(df)

    # Save output
    features_with_segments.to_csv(OUTPUT_SEGMENTS_FILE, index=False)
    segment_metrics.to_csv(OUTPUT_METRICS_FILE, index=False)
    aggregate_behavior_metrics_df.to_csv(OUTPUT_CUSTOMER_BEHAVIOR_METRICS_FILE, index=False)
    aggregate_store_summary_df.to_csv(OUTPUT_CUSTOMER_STORE_METRICS_FILE, index=False)
    aggregate_purchase_trends_df.to_csv(OUTPUT_PURCHASE_TRENDS_FILE, index=False)

    print("Segment data and metrics saved to:")
    print(f"- {OUTPUT_SEGMENTS_FILE}")
    print(f"- {OUTPUT_METRICS_FILE}")
    print(f"- {OUTPUT_CUSTOMER_BEHAVIOR_METRICS_FILE}")
    print(f"- {OUTPUT_CUSTOMER_STORE_METRICS_FILE}")
    print(f"- {OUTPUT_PURCHASE_TRENDS_FILE}")

if __name__ == "__main__":
    main()