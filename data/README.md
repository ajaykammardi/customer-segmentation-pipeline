## 🧬 Customer Data Generation

To simulate customer profiles, run the script below to generate a CSV file of synthetic data.

### Output
A file named `customers_profiles.csv` will be saved in the `data/` directory. It contains:
- `name`: Full name
- `age`: Integer between 18 and 70
- `income`: Annual income between 150000 and 3000000
- `mobile`: Unique mobile number (used as a primary key)
- `gender`: One of Male, Female, or Other

### How to Run

Make sure your environment is activated and required packages are installed (`faker`, `pandas`):

```bash
pip install -r requirements.txt

```bash
python generate_customers_data.py --rows 200 --output customers_profiles.csv --duplicate_ratio 0.1 --missing_ratio 0.2

