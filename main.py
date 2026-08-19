
from db import get_db_connection
from db import app


get_db_connection()


@app.get("/")
def home():
    return {"message": "API is online and connected to MySQL!"}

@app.get("/api/items")
def fetch_view_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Returns rows as JSON dictionaries
    
    try:
        # Fetching data directly from your SQL view
        cursor.execute("SELECT * FROM simple_items_view;")
        items = cursor.fetchall()
        return {"status": "success", "count": len(items), "data": items}
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Query execution failed: {err}")
    
    finally:
        cursor.close()
        conn.close()


@app.get("/api/compute")
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Example computation: Count the number of items in the view
        cursor.execute("SELECT * FROM simple_items_view;")
        result = cursor.fetchone()
        return {"status": "success", "item_count": result['item_count']}
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Query execution failed: {err}")
    
    finally:
        cursor.close()
        conn.close()