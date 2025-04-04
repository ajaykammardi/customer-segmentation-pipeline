-- 📁 Table: customer_segments
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

-- 📁 Table: segment_metrics
CREATE TABLE IF NOT EXISTS segment_metrics (
    segment INT PRIMARY KEY,
    clv FLOAT,
    age FLOAT,
    income FLOAT,
    num_customers INT
);

-- 📁 Table: customer_behavior_metrics
CREATE TABLE IF NOT EXISTS customer_behavior_metrics (
    mobile TEXT PRIMARY KEY,
    total_spent FLOAT,
    avg_transaction_value FLOAT,
    max_purchase_amount FLOAT,
    min_purchase_amount FLOAT,
    purchase_count INT,
    first_purchase DATE,
    last_purchase DATE,
    days_since_first_purchase INT,
    days_since_last_purchase INT
);

-- 📁 Table: customer_store_summary
CREATE TABLE IF NOT EXISTS customer_store_summary (
    mobile TEXT,
    store TEXT,
    total_spent FLOAT,
    visit_count INT,
    PRIMARY KEY (mobile, store)
);

-- 📁 Table: customer_purchase_trends
CREATE TABLE IF NOT EXISTS customer_purchase_trends (
    mobile TEXT,
    month TEXT,
    total_spent FLOAT,
    num_purchases INT,
    PRIMARY KEY (mobile, month)
);
