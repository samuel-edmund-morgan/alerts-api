from fastapi import APIRouter, HTTPException, status, Form
from app.auth import verify_password, create_access_token
import mariadb
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    """Establish a connection to the MariaDB database."""
    try:
        return mariadb.connect(
            user=DB_USER, password=DB_PASSWORD, host="localhost", database="api-db"
        )
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.post("/token")
def generate_token(
    username: str = Form(...),  # Ensure we receive this from form data
    password: str = Form(...)   # Ensure we receive this from form data
):
    """Authenticate user and generate JWT token."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM administrator WHERE username = %s", (username,))
    result = cursor.fetchone()

    if not result or not verify_password(password, result[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Generate and return the access token
    access_token = create_access_token(username)
    return {"access_token": access_token, "token_type": "bearer"}
