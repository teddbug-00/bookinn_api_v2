from pathlib import Path
import time
from fastapi import Depends, FastAPI, Request
from brotli_asgi import BrotliMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware
from sqlalchemy.orm import Session

from app.api.auth.router import auth_router
from app.api.profile.router import user_profile_router
from app.api.listing.router import listing_router
from app.api.reviews.router import reviews_router
from app.api.notifications.router import notifications_router
from app.api.chats.routes import chats_router
from app.websockets.routes import ws
from app.core.config import settings
from app.core.db import get_db
from app.models.user import User
from app.profiling.profiler import ProfilingMiddleware
from app.utils.scheduler import setup_scheduler
from app.core.security.rate_limiter import limiter, rate_limit_exceeded_handler
from app.logging.logger import AppLogger

from docs.views import router

api_version_str = f"/api/{settings.API_VERSION}"

APP_ROOT = Path(__file__).parent.parent

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

setup_scheduler(app)

logger = AppLogger().logger

app.state.limiter = limiter

app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

app.add_exception_handler(
    RateLimitExceeded, rate_limit_exceeded_handler
)

middle_wares = [BrotliMiddleware, SlowAPIASGIMiddleware, ProfilingMiddleware]

for middle_ware in middle_wares:
    if middle_ware == ProfilingMiddleware: # Ignore the profiling middleware for now. Seems to slow down the API
        continue
    app.add_middleware(middle_ware)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.2f}s"
    )
    
    return response


app.include_router(router=router, prefix="/api")
app.include_router(auth_router, prefix=f"{api_version_str}/auth", tags=["Authentication"])
app.include_router(user_profile_router, prefix=f"{api_version_str}/user", tags=["User Profiles"])
app.include_router(listing_router, prefix=f"{api_version_str}/listings", tags=["Listings"])
app.include_router(reviews_router, prefix=f"{api_version_str}/reviews", tags=["Reviews"])
app.include_router(notifications_router, prefix=f"{api_version_str}/notifications", tags=["Notifications"])
app.include_router(chats_router, prefix=f"{api_version_str}/chats", tags=["Chats"])
app.include_router(ws.router)

@app.get("/")
async def index():
    return {"message": "Hello from the BookInn team"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    data = dict()

    num_users = await get_db_stats(db)

    if num_users:
        data["status"] = "healthy"
        data["num_of_users"] = num_users

    return data

async def get_db_stats(db: Session):
    try:
        users = db.query(User).all()

        return len(users) if users else 0
    
    except Exception as e:
        print(e)    


 