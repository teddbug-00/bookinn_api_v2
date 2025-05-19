from fastapi import FastAPI
from brotli_asgi import BrotliMiddleware

from src.api.auth.router import auth_router
from src.api.profile.router import user_profile_router
from src.api.listing.router import listing_router
from src.api.reviews.router import reviews_router
from src.api.notifications.router import notifications_router
from src.core.config import settings
from src.utils.scheduler import setup_scheduler

api_version_str = f"/api/{settings.API_VERSION}"

app = FastAPI()

setup_scheduler(app)

app.add_middleware(BrotliMiddleware)


app.include_router(auth_router, prefix=f"{api_version_str}/auth", tags=["Authentication"])
app.include_router(user_profile_router, prefix=f"{api_version_str}/user", tags=["User Profiles"])
app.include_router(listing_router, prefix=f"{api_version_str}/listings", tags=["Listings"])
app.include_router(reviews_router, prefix=f"{api_version_str}/reviews", tags=["Reviews"])
app.include_router(notifications_router, prefix=f"{api_version_str}/notifications", tags=["Notifications"])

@app.get("/")
async def index():
    return {"message": "Hello from the BookInn team"}

@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
