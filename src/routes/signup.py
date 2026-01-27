from fastapi import APIRouter, HTTPException, Request
import psycopg
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")


def get_db_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def ensure_schema(conn):
    """
    Ensure required tables exist.
    Safe to run multiple times.
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
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
        with get_db_connection() as conn:
            # 1️⃣ Ensure DB is ready
            ensure_schema(conn)

            with conn.cursor() as cur:
                # 2️⃣ Check if user exists
                cur.execute(
                    "SELECT 1 FROM users WHERE username = %s",
                    (username,)
                )
                if cur.fetchone():
                    raise HTTPException(
                        status_code=400,
                        detail="Username already taken"
                    )

                # 3️⃣ Insert user
                cur.execute(
                    """
                    INSERT INTO users (name,email, username, password)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (name, email, username, password)
                )

            conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "User registered successfully",
        "data": {
            "name": name,
            "username": username,
            "email": email
        }
    }
