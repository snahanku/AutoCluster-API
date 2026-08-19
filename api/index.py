from fastapi import FastAPI, HTTPException
import mysql.connector
import os

app = FastAPI()

# Wrap app for serverless execution
from mangum import Mangum
handler = Mangum(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

@app.get("/api/items")
def fetch_items():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM simple_items_view;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"status": "success", "data": data}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database connection error: {err}")