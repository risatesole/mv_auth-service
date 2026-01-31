from fastapi import APIRouter, HTTPException, Request
from utils.hasher import hasher
from fastapi.responses import JSONResponse
import re
from config.env import ENVIRONMENTVARIABLES
from config.config import database

router = APIRouter(prefix="/api/auth", tags=["auth"])

DB_FILE = ENVIRONMENTVARIABLES["SQLITE3DBLOCATION"]

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

    # reject short usernames
    MIN_USERNAME_LEN = 3

    if len(username) < MIN_USERNAME_LEN:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Username must be at least {MIN_USERNAME_LEN} characters long",
            }
        )

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
        conn = database.get_connection()

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
