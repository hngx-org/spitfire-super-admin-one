import psycopg2
from psycopg2 import sql
import os
import random
import json
from uuid import uuid4
import datetime
import string
from decimal import Decimal
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

    # Insert data to the 'product_category' table
    # cur.execute(
    #    """
    #    INSERT INTO product_category (id, name, parent_category_id, status)
    #     VALUES ('0', 'spitfire', NULL, 'pending')
    # """
    # )

    # Insert data to the 'user_product_rating' table
    # cur.execute(
    #     """
    #     INSERT INTO user_product_rating (id, user_id, product_id, rating)
    #     VALUES ('0', 'de73e148-c1dc-41ab-a44a-acbd59542cf6', 'de73e148-c1dc-41ab-a44a-acbd59542cf6', 5)
    # """
    # )

    # conn.commit()

    # List the columns in 'product_logs' table
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'product_logs'
    """
    )

    # Fetch the results
    results = cur.fetchall()

    # Print the results
    print(f"Columns in 'product_logs' table: {results}")


    # SQL query to insert data into the 'product' table
    insert_query = psycopg2.sql.SQL(
        """
        INSERT INTO product (id, shop_id, name, description, quantity, category_id, price, discount_price, tax, admin_status, is_deleted, rating_id, is_published, currency, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    )

    # Data to be inserted
    data = [
        (
            uuid4().hex,
            "de73e148-c1dc-41ab-a44a-acbd59542cf6",
            "Gucci Dress",
            "A beautiful dress",
            10,
            0,
            100.00,
            90.00,
            5.00,
            "pending",
            "active",
            0,
            True,
            "USD",
            "2022-10-17 12:00:00",
            "2022-10-17 13:00:00",
        ),
    ]

    # Execute the query
    cur.execute(insert_query, data[0])

    # Commit the changes to the database
    conn.commit()

    table_name = "product"

    # Print the results
    print(f"Inserted data into table {table_name}")
    print(f"Inserted data: {data}")

except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()

