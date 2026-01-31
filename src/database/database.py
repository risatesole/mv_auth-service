import sqlite3
from config.env import ENVIRONMENTVARIABLES

class Database:
    def __init__(self):
        self.db_path = ENVIRONMENTVARIABLES["SQLITE3DBLOCATION"]

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_db_migration(self):
        print("executing database migration")
        conn = self.get_connection()
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
        pass
