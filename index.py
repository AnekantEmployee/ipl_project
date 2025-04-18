import pandas as pd
import pymysql
import numpy as np

# Load your DataFrame
df = pd.read_csv("datasets/deliveries_cleaned.csv")

# Remove the unwanted first column (Unnamed: 0)
# df = df.iloc[:, 1:]  # Correct way to select all rows and columns starting from index 1

# Replace "NR" with None (NULL in SQL)
df.replace("NR", None, inplace=True)

# Database connection details
host = "localhost"
user = "root"
password = "root"
database_name = "ipl_data"
table_name = "deliveries"

# Initialize connection variable
conn = None

try:
    # Print sample data for verification
    print("Sample data to be inserted:")
    print(df.head(2))
    
    # Establish connection
    conn = pymysql.connect(
        host=host, 
        port=3306, 
        user=user, 
        password=password, 
        database=database_name
    )
    cursor = conn.cursor()

    # Prepare SQL with backtick-quoted columns
    columns = ", ".join([f"`{col}`" for col in df.columns])
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

    # Convert DataFrame to list of tuples, handling NULL values
    values = [tuple(None if pd.isna(x) else x for x in row) 
              for row in df.to_numpy()]

    # Execute the insert
    cursor.executemany(insert_sql, values)
    conn.commit()
    
    print(f"\nSuccessfully inserted {len(df)} rows into {table_name}")

except Exception as e:
    print(f"\nError occurred: {e}")
    if conn:  # Check if connection was established before rollback
        conn.rollback()
finally:
    if conn:  # Safely close connection if it exists
        conn.close()