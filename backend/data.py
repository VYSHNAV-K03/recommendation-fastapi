import sqlite3
import pandas as pd

DB_PATH = "dummy.db"

def get_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")  # Use WAL to allow concurrent read/write
    conn.execute("PRAGMA synchronous=OFF")   # Improves speed, OK for testing
    return conn


def get_product_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def get_user_data():
    """Fetch user data from the database."""
    conn = get_connection()
    query = "SELECT * FROM users"
    user_data = pd.read_sql_query(query, conn)
    conn.close()
    return user_data

def get_user_item_data():
    """Fetch user-item interaction data from the database."""
    conn = get_connection()
    query = "SELECT * FROM user_item_interactions"
    user_item_data = pd.read_sql_query(query, conn)
    conn.close()
    return user_item_data

def add_product(product: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (item_id, name, category, price, brand, rating, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product["item_id"],
            product["name"],
            product["category"],
            product["price"],
            product["brand"],
            product["rating"],
            product["image_url"]
        ))
        conn.commit()
        # Now read using same connection and cursor
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        return {"message": "Product added successfully", "data": data}
        # return {"message": "Product added successfully"}
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        conn.commit()
        conn.close()

def add_user(user: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (user_id, name, age, location)
            VALUES (?, ?, ?, ?)
        """, (
            user["user_id"],
            user["name"],
            user["age"],
            user["location"]
        ))
        conn.commit()
        return {"message": "User added successfully"}
    except sqlite3.IntegrityError as e:
        return {"error": str(e)}
    finally:
        conn.close()
