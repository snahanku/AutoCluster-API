from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI(title="Items View API")

# Database configuration using your restricted view-only user
DB_CONFIG = {
    "host": "localhost",
    "user": "api_readonly",
    "password": "Bengali@09",  # Must match the password set in MySQL
    "database": "testdb"
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database connection error: {err}")