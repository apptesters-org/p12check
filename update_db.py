import pandas as pd
import sqlite3

# Read data from Excel file
excel_file = 'device_data.xlsx'
df = pd.read_excel(excel_file)

# Convert datetime columns to strings
datetime_columns = ['certificate_purchase_date', 'certificate_expiry_date', 'developer_account_renewal_date']
for col in datetime_columns:
    df[col] = df[col].astype(str)

# Connect to the SQLite database
conn = sqlite3.connect('device_data.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS devices (
        udid TEXT PRIMARY KEY,
        certificate_purchase_date TEXT,
        plan TEXT,
        certificate_expiry_date TEXT,
        developer_account_name TEXT,
        developer_account_renewal_date TEXT
    )
''')

# Insert data into the table
for index, row in df.iterrows():
    c.execute('''
        INSERT OR REPLACE INTO devices (udid, certificate_purchase_date, plan, certificate_expiry_date, developer_account_name, developer_account_renewal_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['udid'], row['certificate_purchase_date'], row['plan'], row['certificate_expiry_date'], row['developer_account_name'], row['developer_account_renewal_date']))

# Commit and close the connection
conn.commit()

# Check if data was inserted
c.execute('SELECT COUNT(*) FROM devices')
count = c.fetchone()[0]
print(f'{count} records inserted into the database.')

conn.close()
