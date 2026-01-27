from fastapi import FastAPI
from routes.signup import router as signup_router

app = FastAPI()

app.include_router(signup_router)
