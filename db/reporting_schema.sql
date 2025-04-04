-- customer_segments
CREATE TABLE customer_segments (
    mobile BIGINT, 
    clv DOUBLE PRECISION, 
    avg_purchase_amount DOUBLE PRECISION, 
    max_purchase_amount DOUBLE PRECISION, 
    min_purchase_amount DOUBLE PRECISION, 
    purchase_count BIGINT, 
    last_purchase TEXT, 
    first_purchase TEXT, 
    age DOUBLE PRECISION, 
    income DOUBLE PRECISION, 
    gender BIGINT, 
    days_since_last_purchase DOUBLE PRECISION, 
    purchase_frequency DOUBLE PRECISION, 
    days_since_first_purchase DOUBLE PRECISION, 
    segment BIGINT
    );

-- segment_metrics
CREATE TABLE segment_metrics (
    segment BIGINT, 
    clv DOUBLE PRECISION, 
    age DOUBLE PRECISION, 
    income DOUBLE PRECISION, 
    num_customers BIGINT);

-- customer_behavior_metrics
CREATE TABLE customer_behavior_metrics (
    mobile BIGINT, 
    total_spent DOUBLE PRECISION, 
    avg_transaction_value DOUBLE PRECISION, 
    max_purchase_amount DOUBLE PRECISION, 
    min_purchase_amount DOUBLE PRECISION, 
    purchase_count BIGINT, 
    first_purchase TEXT, 
    last_purchase TEXT, 
    days_since_first_purchase DOUBLE PRECISION, 
    days_since_last_purchase DOUBLE PRECISION
    );

-- customer_store_summary
CREATE TABLE customer_store_summary (
    mobile BIGINT, 
    store TEXT, 
    total_spent DOUBLE PRECISION, 
    visit_count BIGINT
    );

-- customer_purchase_trends
CREATE TABLE customer_purchase_trends (
    mobile BIGINT, 
    month TEXT, 
    total_spent DOUBLE PRECISION, 
    num_purchases BIGINT
    );
