from fastapi import APIRouter, HTTPException, Request
import sqlite3
import os
from utils.hasher import hasher  # your hasher.py

router = APIRouter(prefix="/api/auth", tags=["auth"])

DB_FILE = os.getenv("DB_FILE", "users.sqlite3")


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  
    return conn


def ensure_schema(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()


@router.post("/signup")
async def signup(request: Request):
    data = await request.json()

    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    try:
        conn = get_db_connection()
        ensure_schema(conn)

        result = conn.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone()

        if result:
            raise HTTPException(status_code=400, detail="Username already taken")

        hashed_password = hasher(password)

        cursor = conn.execute(
            """
            INSERT INTO users (name, email, username, password)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, username, hashed_password)
        )
        conn.commit()
        
        user_id = cursor.lastrowid

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return {
        "message": "User registered successfully",
        "data": {
            "userid": user_id,
            "name": name,
            "username": username,
            "email": email
        }
    }
