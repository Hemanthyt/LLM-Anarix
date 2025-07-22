import os
import sqlite3
import pandas as pd

# Database location
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS eligibility (
    eligibility_datetime_utc TEXT,
    item_id TEXT,
    eligibility TEXT,
    message TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ad_sales (
    date TEXT,
    item_id TEXT,
    ad_sales REAL,
    impressions INTEGER,
    ad_spend REAL,
    clicks INTEGER,
    units_sold INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS total_sales (
    date TEXT,
    item_id TEXT,
    total_sales REAL,
    total_units_ordered INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS  user (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    signup_date DATE NOT NULL,
    last_login DATE,
    is_active BOOLEAN NOT NULL CHECK (is_active IN (0, 1)),
    role TEXT CHECK (role IN ('admin', 'user', 'guest', 'moderator'))
);

''')


# Load CSVs
eligibility_df = pd.read_csv(os.path.join(DATA_PATH, "eligibility_table.csv"))
ad_sales_df = pd.read_csv(os.path.join(DATA_PATH, "product_ad_sales.csv"))
total_sales_df = pd.read_csv(os.path.join(DATA_PATH, "product_total_sales.csv"))

# # Insert data
eligibility_df.to_sql('eligibility', conn, if_exists='replace', index=False)
ad_sales_df.to_sql('ad_sales', conn, if_exists='replace', index=False)
total_sales_df.to_sql('total_sales', conn, if_exists='replace', index=False)

user = pd.read_csv(os.path.join(DATA_PATH, "user.csv"))
user.to_sql('user', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("✅ Database seeded successfully.")
