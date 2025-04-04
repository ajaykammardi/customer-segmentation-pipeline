import pandas as pd
import numpy as np
import random
import argparse
from faker import Faker

def generate_mobile_number():
    """Generate a valid mobile number."""
    return f"+91{random.randint(6000000000, 9999999999)}"

def generate_customer_profile_data(n=1000, duplicate_ratio=0.05, missing_ratio=0.1):
    fake = Faker('en_IN')
    Faker.seed(42)
    random.seed(42)
    np.random.seed(42)
    
    genders = ['Male', 'Female', 'Other']
    data = []

    for _ in range(n):
        profile = {
            'name': fake.name(),
            'age': random.choice([random.randint(18, 70), None]) if random.random() < missing_ratio else random.randint(18, 70),
            'income': round(random.uniform(150000, 3000000), 2),
            'mobile': generate_mobile_number(),
            'gender': random.choice(genders)
        }
        data.append(profile)

    # Introduce duplicates
    duplicates = random.choices(data, k=int(n * duplicate_ratio))
    data += duplicates

    # Shuffle data
    random.shuffle(data)

    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic customer profile data.")
    parser.add_argument('--rows', type=int, default=1000, help='Number of customer profiles to generate')
    parser.add_argument('--output', type=str, default='data/customer_profiles.csv', help='Output CSV file name')
    parser.add_argument('--duplicate_ratio', type=float, default=0.05, help='Fraction of duplicates to include')
    parser.add_argument('--missing_ratio', type=float, default=0.1, help='Fraction of missing values in age')

    args = parser.parse_args()

    df = generate_customer_profile_data(
        n=args.rows,
        duplicate_ratio=args.duplicate_ratio,
        missing_ratio=args.missing_ratio
    )

    df.to_csv(args.output, index=False)
    print(f"Generated {len(df)} records and saved to '{args.output}'")

if __name__ == '__main__':
    main()

