import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv('.env')

# Database connection parameters
db_params = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
}

# SQL query to insert data into the 'product' table
insert_query = sql.SQL("""
    INSERT INTO product (id, shop_id, name, description, quantity, category_id, price, discount_price, tax, admin_status, is_deleted, rating_id, is_published, currency, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

# Data to be inserted
data_to_insert = [
    (uuid4().hex, '3793258b-859b-41ef-97d7-cc4f1dda7c05', 'Gucci Dress', 'A beautiful dress', 10, 7, 100.00, 90.00, 5.00, 'pending', 'active', 1, True, 'USD', '2022-10-17 12:00:00', '2022-10-17 13:00:00'),
    (uuid4().hex, '3793258b-859b-41ef-97d7-cc4f1dda7c05', 'Chanel Dress', 'A designer\'s dress', 15, '8', 150.00, 130.00, 8.00, 'approved', 'active', 2, True, 'USD', '2022-10-17 14:00:00', '2022-10-17 15:00:00')
]


conn = None
cur = None

print("Database Connection Parameters:", db_params)

try:
    print("Connecting to the PostgreSQL database...")
    # Establish a connection to the database
    conn = psycopg2.connect(**db_params)
    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Insert data into the 'user' table
    cur.executemany(insert_query, data_to_insert)
    print("Data successfully inserted into the 'user' table.")

    # Commit the transaction
    conn.commit()

except psycopg2.Error as e:
    print("Error inserting data into the 'user' table:", e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()

#TEST QUERIES
# # SQL query to insert data into the 'product_category' table
# insert_query = sql.SQL("""
#     INSERT INTO "product_category" ("name", "parent_category_id", "status")
#     VALUES (%s, %s, %s)
# """)

# # Data to be inserted
# data_to_insert = [
#     ('Electronics', 1, 'complete'),
#     ('Fashion', 1, 'complete')
# ]

# SQL query to insert data into the 'user' table
# insert_query = sql.SQL("""
#     INSERT INTO "user" (id, username, first_name, last_name, email, section_order, password, provider, is_verified, two_factor_auth, profile_pic, refresh_token, created_at)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """)

# # Data to be inserted
# data_to_insert = [
#     (uuid4().hex, "Opalina", "Hutchcraft", "ohutchcraft0@berkeley.edu", "ohutchcraft0@wp.com", "section_value", "password_value", "provider_value", True, False, "http://dummyimage.com/236x100.png/ff4444/ffffff", "refresh_token_value", "10/17/2022"),
#     (uuid4().hex, "Bartram", "Scrange", "bscrange1@utexas.edu", "bscrange1@sakura.ne.jp", "section_value", "password_value", "provider_value", True, True, "http://dummyimage.com/137x100.png/ff4444/ffffff", "refresh_token_value", "8/28/2023")
# ]
# # SQL query to insert data into the 'shop' table
# insert_query = sql.SQL("""
#     INSERT INTO shop (id, merchant_id, name, policy_confirmation, restricted, admin_status, is_deleted, reviewed, rating, created_at, updated_at)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """)

# # Data to be inserted
# data_to_insert = [
#     (uuid4().hex, 'd08ba1da-10b1-4064-a206-4299b35bc087', 'Opalina Shop', True, 'no', 'pending', 'active', False, 5.0, "10/17/2022 12:00:00", "10/17/2022 13:00:00"),
# (uuid4().hex, 'c2ee45b9-d6d1-4e72-af00-b4164fb1c2a7', 'Bartram Shop', False,'no', 'pending', 'active', False, 5.0, "10/17/2022 12:00:00", "10/17/2022 13:00:00")
# ]