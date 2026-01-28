from fastapi import APIRouter, HTTPException, Request
import sqlite3
import os
from utils.hasher import hasher
from fastapi.responses import JSONResponse
import re

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
            passwordhash TEXT NOT NULL
        );
    """)
    conn.commit()


@router.post("/signup")
async def signup(request: Request):
    data = await request.json()

    required_fields = ["name", "email", "username", "password"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Missing fields: {', '.join(missing_fields)}",
            }
        )

    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # reject username with spaces
    if any(char.isspace() for char in username):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Username must not contain spaces",
            }
        )
    
    # reject username with special characters:
    if re.search(r"[^a-zA-Z0-9_]", username):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Username contains invalid characters",
            }
        )  


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
            INSERT INTO users (name, email, username, passwordhash)
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

    return JSONResponse(status_code=201,
        content={
            "message": "User created successfully",
            "success": True,
            "data": {
                "userid": user_id,
                "name": name,
                "username": username,
                "email": email
            }
        }
    )