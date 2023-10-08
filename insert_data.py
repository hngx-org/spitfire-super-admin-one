import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv('.env')

# Database connection parameters
db_params = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
}

# # SQL query to insert data into the 'user' table
# insert_query = sql.SQL("""
#     INSERT INTO "user" (id, username, first_name, last_name, email, section_order, password, provider, is_verified, two_factor_auth, profile_pic, refresh_token, created_at)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """)

# # Data to be inserted
# data_to_insert = [
#     ("3b875433-9713-4b58-bcfc-bfed12013da1", "Opalina", "Hutchcraft", "ohutchcraft0@berkeley.edu", "ohutchcraft0@wp.com", "section_value", "password_value", "provider_value", True, False, "http://dummyimage.com/236x100.png/ff4444/ffffff", "refresh_token_value", "10/17/2022"),
#     ("e03ada4b-d081-4f00-9694-c71a5be1d6b2", "Bartram", "Scrange", "bscrange1@utexas.edu", "bscrange1@sakura.ne.jp", "section_value", "password_value", "provider_value", True, True, "http://dummyimage.com/137x100.png/ff4444/ffffff", "refresh_token_value", "8/28/2023")
# ]
# SQL query to insert data into the 'user' table
insert_query = sql.SQL("""
    INSERT INTO shop (id, merchant_id, name, policy_confirmation, restricted, admin_status, is_deleted, reviewed, rating, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

# Data to be inserted
data_to_insert = [
    ('3b875433-9713-4b58-bcfc-bfed12013da2', '3b875433-9713-4b58-bcfc-bfed12013da1', 'Shop Name 1', True, 'no', 'pending', 'active', False, 5.0, "10/17/2022 12:00:00", "10/17/2022 13:00:00"),
('3b875433-9713-4b58-bcfc-bfed12013da3', 'e03ada4b-d081-4f00-9694-c71a5be1d6b2', 'Shop Name 2', False,'no', 'pending', 'active', False, 5.0, "10/17/2022 12:00:00", "10/17/2022 13:00:00")
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

