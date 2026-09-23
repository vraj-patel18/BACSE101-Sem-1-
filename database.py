import mysql.connector
from mysql.connector import Error

from config import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


# =========================================
# CONNECT TO MYSQL
# =========================================

def get_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        return connection

    except Error as e:

        print("Database connection error:", e)

        return None


# =========================================
# FETCH ONE RECORD
# =========================================

def fetch_one(query, values=()):
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        return result

    except Error as e:
        print("Database error:", e)
        return None

    finally:
        cursor.close()
        connection.close()


# =========================================
# FETCH ALL RECORDS
# =========================================

def fetch_all(query, values=()):
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, values)
        result = cursor.fetchall()
        return result

    except Error as e:
        print("Database error:", e)
        return []

    finally:
        cursor.close()
        connection.close()


# =========================================
# EXECUTE INSERT / UPDATE / DELETE
# =========================================

def execute_query(
    query,
    values=(),
    return_id=False
):

    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()

    try:
        cursor.execute(query, values)
        connection.commit()
        if return_id:
            return cursor.lastrowid
        return cursor.rowcount

    except Error as e:
        connection.rollback()
        print("Database error:", e)
        return None

    finally:
        cursor.close()
        connection.close()