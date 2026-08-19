import os
from fastapi import FastAPI, HTTPException
import mysql.connector
from mangum import Mangum
from dotenv import load_dotenv

# Load local .env file if running locally
load_dotenv()

app = FastAPI()

# Serverless handler for Vercel
handler = Mangum(app)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "api_readonly"),
            password=os.getenv("DB_PASSWORD", "Bengali@09"),
            database=os.getenv("DB_NAME", "testdb"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return connection
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database connection error: {err}")

@app.get("/api/items")
def fetch_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM simple_items_view;")
        data = cursor.fetchall()
        return {"status": "success", "data": data}
    finally:
        cursor.close()
        conn.close()