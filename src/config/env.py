import os

ENVIRONMENTVARIABLES  = {
    "SQLITE3DBLOCATION": os.getenv("DB_FILE", "users.sqlite3")
}
