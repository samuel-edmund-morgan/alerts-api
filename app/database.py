import mariadb
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    try:
        return mariadb.connect(
            user=DB_USER, password=DB_PASSWORD, host="localhost", database="api-db"
        )
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")