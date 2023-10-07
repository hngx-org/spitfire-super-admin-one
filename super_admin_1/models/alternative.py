import psycopg2, os
from psycopg2 import sql



# ++++++++++++++++++++++++++++++THIS IS A TEST SCENARIO!++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Database:
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            print("Error executing query:", error)

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as error:
            print("Error fetching data:", error)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

# Example usage:
if __name__ == "__main__":
    # Database configuration
    host = os.environ.get("host")
    dbname = os.environ.get("dbname")
    user = os.environ.get("user")
    port = os.environ.get("port")
    password =  os.environ.get("password")

    # Create a Database instance
    db = Database(dbname, user, password, host, port)

    # Example queries
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255)
    )
    """

    insert_data_query = """
    INSERT INTO users (username, email) VALUES (%s, %s)
    """

    select_data_query = "SELECT * FROM public.shop"

    # Execute queries
    # db.execute_query(create_table_query)
    # db.execute_query(insert_data_query, ("john_doe", "john@example.com"))
    # db.execute_query(insert_data_query, ("jane_smith", "jane@example.com"))

    # Fetch and print data
    shop = db.fetch_data(select_data_query)
    print("shop:")
    print(shop)
    for user in shop:
        print(user)

    # Close the database connection
    db.close_connection()