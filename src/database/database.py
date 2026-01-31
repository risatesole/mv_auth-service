import sqlite3
from config.env import ENVIRONMENTVARIABLES

class Database:
    def __init__(self):
        self.db_path = ENVIRONMENTVARIABLES["SQLITE3DBLOCATION"]

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
