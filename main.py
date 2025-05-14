import uvicorn

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.api.auth.router import auth_router
from src.api.profile.router import user_profile_router
from src.api.listing.router import listing_router
from src.api.reviews.router import reviews_router

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"api/auth/token")

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_profile_router, prefix="/api/user", tags=["User Profiles"])
app.include_router(listing_router, prefix="/api/listings", tags=["Listings"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["Reviews"])

@app.get("/")
async def index():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
