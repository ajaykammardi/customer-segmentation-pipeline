import pandas as pd
import requests
import re

CUSTOMER_FILE = "data/customer_profiles.csv"
PURCHASE_API_URL = "http://127.0.0.1:8000/purchase-history"

def is_valid_mobile(mobile):
    """
    Check if the mobile number is at least 10 digits and only contains numbers.
    """
    if pd.isna(mobile):
        return False
    mobile = str(mobile).strip()
    return bool(re.fullmatch(r"\d{10,}", mobile))

def extract_customers():
    """
    Load and clean customer data from CSV:
    - Remove rows with missing, blank, or invalid mobile numbers
    - Remove duplicates
    """
    print("Reading customer data from CSV...")
    df = pd.read_csv(CUSTOMER_FILE)

    original_count = len(df)

    # Drop missing or blank mobile numbers
    df = df[df['mobile'].notna()]
    df = df[df['mobile'].astype(str).str.strip() != ""]

    # Validate format (e.g., 10+ digits)
    df = df[df['mobile'].apply(is_valid_mobile)]

    # Drop duplicates (based on mobile)
    df = df.drop_duplicates(subset='mobile')

    final_count = len(df)
    print(f"Valid customers loaded: {final_count} (removed {original_count - final_count})")

    return df

def extract_purchases(mobiles):
    """
    Request purchase history for a list of mobile numbers.
    """
    print("Requesting purchase history from API...")
    response = requests.post(PURCHASE_API_URL, json={"mobiles": mobiles})
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}")
    return pd.DataFrame(response.json()["purchases"])

def join_data(customers_df, purchases_df):
    """
    Merge purchase and customer data on 'mobile'.
    """
    print("Joining customer and purchase data...")

    # Ensure both columns are strings
    customers_df["mobile"] = customers_df["mobile"].astype(str)
    purchases_df["mobile"] = purchases_df["mobile"].astype(str)

    return pd.merge(customers_df, purchases_df, on="mobile", how="left")

# Optional: standalone testable main
if __name__ == "__main__":
    customers_df = extract_customers()
    mobiles = customers_df["mobile"].astype(str).tolist()
    purchases_df = extract_purchases(mobiles)
    joined_df = join_data(customers_df, purchases_df)
    joined_df.to_csv("data/joined_data.csv", index=False)
    print("Joined data written to data/joined_data.csv")
