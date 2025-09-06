from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import uvicorn
    
load_dotenv()  # Load .env file

DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")

app = FastAPI()

try:
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME   ,
        sslmode="require"
    )
    print("Connected to Supabase successfully!")
except Exception as e:
    print("Failed to connect:", e)
    conn = None

@app.get("/sns-data")
def get_sns_data():
    if not conn:
        return {"error": "Database connection not available"}
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM SNS_Data;")
            rows = cur.fetchall()
            return rows
    except Exception as e:
        return {"error": str(e)}


@app.get("/test")
def test():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)


