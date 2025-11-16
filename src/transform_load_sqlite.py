"""
Step 3 - Transform dataset into Dim/Fact tables
and load into SQLite database.

Revised to use dim_location instead of dim_store.
"""

import os
import sqlite3
import pandas as pd

#####################    set vars    ############################

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(PROJECT_ROOT, "src/data_raw")
CSV_PATH = os.path.join(DATA_DIR, "supermarket_sales.csv")
DB_PATH = os.path.join(PROJECT_ROOT, "supermarket.db")
DDL_PATH = os.path.join(PROJECT_ROOT, "src/sql/create_tables.sql")

#####################    csv load    ############################

def load_data():
    df = pd.read_csv(CSV_PATH)
    return df

#####################   create db/tables    ############################

def create_database():
    conn = sqlite3.connect(DB_PATH)
    with open(DDL_PATH, "r") as f:
        ddl_script = f.read()
    conn.executescript(ddl_script)
    conn.commit()
    conn.close()

#####################    location dim   ############################
def build_dim_location(df):
    dim_location = df[["Branch", "City"]].drop_duplicates().reset_index(drop=True)
    dim_location = dim_location.rename(columns={
        "Branch": "branch",
        "City": "city"
    })
    dim_location["location_id"] = dim_location.index + 1
    return dim_location[["location_id", "branch", "city"]]

#####################    product dim    ############################
def build_dim_product(df):
    dim_product = df[["Product line"]].drop_duplicates().reset_index(drop=True)
    dim_product = dim_product.rename(columns={"Product line": "product_line"})
    dim_product["product_id"] = dim_product.index + 1
    return dim_product[["product_id", "product_line"]]

#####################    customer dim    ############################
def build_dim_customer_segment(df):
    dim_seg = df[["Customer type", "Gender"]].drop_duplicates().reset_index(drop=True)
    dim_seg = dim_seg.rename(columns={
        "Customer type": "customer_type",
        "Gender": "gender"
    })
    dim_seg["customer_segment_id"] = dim_seg.index + 1
    return dim_seg[["customer_segment_id", "customer_type", "gender"]]

#####################    fact table function    ############################
def build_fact(df, dim_location, dim_product, dim_seg):
    df = df.rename(columns={
        "Invoice ID": "invoice_id",
        "Product line": "product_line",
        "Customer type": "customer_type",
        "Gender": "gender",
        "Unit price": "unit_price",
        "Tax 5%": "tax_amount",
        "Total": "total_amount",
        "Date": "date",
        "Time": "time",
        "Payment": "payment",
        "Rating": "rating",
        "gross income": "gross_income",
        "gross margin percentage": "gross_margin_pct"
    })

    # Join location
    df = df.merge(
        dim_location,
        left_on=["Branch", "City"],
        right_on=["branch", "city"],
        how="left"
    )

    # Join product
    df = df.merge(dim_product, on="product_line", how="left")

    # Join customer segment
    df = df.merge(dim_seg, on=["customer_type", "gender"], how="left")

    fact = df[[
        "invoice_id",
        "location_id",
        "product_id",
        "customer_segment_id",
        "date",
        "time",
        "unit_price",
        "Quantity",
        "tax_amount",
        "total_amount",
        "payment",
        "cogs",
        "gross_margin_pct",
        "gross_income",
        "rating"
    ]]

    fact = fact.rename(columns={"Quantity": "quantity"})

    return fact

#####################    sqllite load    ############################
def load_to_sqlite(dim_location, dim_product, dim_seg, fact):
    conn = sqlite3.connect(DB_PATH)

    dim_location.to_sql("dim_location", conn, if_exists="replace", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)
    dim_seg.to_sql("dim_customer_segment", conn, if_exists="replace", index=False)
    fact.to_sql("fact_sales", conn, if_exists="replace", index=False)

    conn.close()
    print("Data loaded")


#####################    create view    ############################
def create_report_view():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(os.path.join(PROJECT_ROOT, "src/sql/report_product_performance.sql")) as f:
        query = f.read()

    cursor.executescript(f"""
        DROP VIEW IF EXISTS vw_product_performance;
        CREATE VIEW vw_product_performance AS
        {query}
    """)

    conn.commit()
    conn.close()

#####################    main    ############################
if __name__ == "__main__":
    df = load_data()
    create_database()

    dim_location = build_dim_location(df)
    dim_product = build_dim_product(df)
    dim_seg = build_dim_customer_segment(df)
    fact = build_fact(df, dim_location, dim_product, dim_seg)

    load_to_sqlite(dim_location, dim_product, dim_seg, fact)
    create_report_view()

