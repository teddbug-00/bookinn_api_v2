from fastapi import FastAPI
from src.api.auth.router import auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication endpoints"])

@app.get("/")
async def index():
    return {"message": "Welcome to the API"}