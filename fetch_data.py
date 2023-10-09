import psycopg2
import os
import json
from decimal import Decimal
import datetime

from dotenv import load_dotenv

load_dotenv(".env")

# Database connection parameters
db_params = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
}

try:
    # Establish a connection to the database
    conn = psycopg2.connect(**db_params)
    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Ask the user for input
    table_name = input("Enter the name of the table to fetch data from: ")

    # Ensure the user input is not empty
    if not table_name:
        raise ValueError("Table name cannot be empty")
    else:
        table_name = table_name.lower()
        # Check if the table exists
        cur.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
            """,
            (table_name,),
        )
        table_exists = cur.fetchone()[0]
        if not table_exists:
            raise ValueError(f"Table {table_name} does not exist")

    # SQL query to select all users
    select_query = f"SELECT * FROM {table_name};"

    # Execute the query
    cur.execute(select_query)

    # Fetch all rows from the result set
    table = cur.fetchall()

    if not table:
        print(f"The table {table_name} is empty")
        exit()

    # Print the rows in the table
    print(f"Rows in the table {table_name}:")
    for row in table:
        # Create a dictionary to store the row data
        row_data = {}
        for col, value in zip([col[0] for col in cur.description], row):
            # Convert Decimal to float and Fix datetime
            if isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            row_data[col] = value
        # Print the dictionary as well-formatted JSON
        print(json.dumps(row_data, indent=4))

except psycopg2.Error as e:
    print(f"Error: Could not fetch data from the table {table_name}", e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()

