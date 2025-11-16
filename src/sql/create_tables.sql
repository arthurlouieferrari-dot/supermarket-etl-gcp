-- ============================
-- Dimension: Location
-- ============================
CREATE TABLE IF NOT EXISTS dim_location (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch TEXT NOT NULL,
    city TEXT NOT NULL,
    UNIQUE(branch, city)
);

-- ============================
-- Dimension: Product
-- ============================
CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_line TEXT NOT NULL UNIQUE
);

-- ============================
-- Dimension: Customer Segment
-- ============================
CREATE TABLE IF NOT EXISTS dim_customer_segment (
    customer_segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_type TEXT NOT NULL,
    gender TEXT NOT NULL,
    UNIQUE(customer_type, gender)
);

-- ============================
-- Fact: Sales
-- ============================
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id TEXT NOT NULL,

    location_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    customer_segment_id INTEGER NOT NULL,

    date TEXT NOT NULL,
    time TEXT NOT NULL,

    unit_price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    tax_amount REAL NOT NULL,
    total_amount REAL NOT NULL,
    payment TEXT NOT NULL,

    cogs REAL,
    gross_margin_pct REAL,
    gross_income REAL,
    rating REAL,

    FOREIGN KEY(location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY(customer_segment_id) REFERENCES dim_customer_segment(customer_segment_id)
);
