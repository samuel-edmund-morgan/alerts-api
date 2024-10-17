from fastapi import APIRouter, HTTPException, status
from app.auth import verify_password, create_access_token
import mariadb
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    return mariadb.connect(user=DB_USER, password=DB_PASSWORD, host="localhost", database="api-db")

@router.post("/token")
def generate_token(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM administrator WHERE username = %s", (username,))
    result = cursor.fetchone()

    if not result or not verify_password(password, result[0]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(username)
    return {"access_token": access_token, "token_type": "bearer"}
