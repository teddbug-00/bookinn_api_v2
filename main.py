import uvicorn

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.api.auth.router import auth_router
from src.api.profile.router import user_profile_router

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"api/auth/token")

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication endpoints"])
app.include_router(user_profile_router, prefix="/api/user", tags=["User profile endpoints"])

@app.get("/")
async def index():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
