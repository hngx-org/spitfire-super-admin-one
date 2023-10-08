import psycopg2
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

try:
    # Establish a connection to the database
    conn = psycopg2.connect(**db_params)
    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # SQL query to select all users
    select_query = "SELECT * FROM \"user\";"

    # Execute the query
    cur.execute(select_query)

    # Fetch all rows from the result set
    users = cur.fetchall()

    # Print the users
    for user in users:
        print(user)

except psycopg2.Error as e:
    print("Error: Unable to fetch data from the 'user' table:", e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()
