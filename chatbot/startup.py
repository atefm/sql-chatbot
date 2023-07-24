import psycopg2
import random
from datetime import datetime, timedelta
import os


def populate_db_with_random_data():
# Get the environment variables
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    dbname = os.getenv('POSTGRES_DB')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')


# Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor object
    cur = conn.cursor()

    # Create the 'trades' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS  trades (
            trade_id SERIAL PRIMARY KEY,
            trade_date DATE NOT NULL,
            security VARCHAR(50) NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Commit the transaction
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM trades")
    row_count = cur.fetchone()[0]

    # If the table is empty, populate it with random data
    if row_count == 0:
    # Define a list of possible securities
        securities = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB']

        # Populate the 'trades' table with random data
        for _ in range(1000):  # change the range to the number of rows you want to generate
            trade_date = datetime.now() - timedelta(days=random.randint(0, 365))
            security = random.choice(securities)
            quantity = random.randint(1, 100)
            price = random.uniform(100, 200)

            # Insert the data into the 'trades' table
            cur.execute("""
                INSERT INTO trades (trade_date, security, quantity, price) 
                VALUES (%s, %s, %s, %s)
            """, (trade_date, security, quantity, price))

        # Commit the transaction
        conn.commit()

    # Close the cursor and the connection
    cur.close()
    conn.close()

