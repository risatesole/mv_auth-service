from fastapi import FastAPI
from routes.signup import router as signup_router
from config.config import database

database.execute_db_migration()

app = FastAPI()

app.include_router(signup_router)
