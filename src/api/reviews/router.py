from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from src.api.reviews.handlers.create import create_review
from src.core.db import get_db
from src.core.security.tokens import get_current_user_id
from src.schemas.review import ReviewCreateRequest

reviews_router = APIRouter()

@reviews_router.post("/{listing_id}/add", status_code=status.HTTP_201_CREATED)
async def add_review(
    listing_id: str,
    review_data: ReviewCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()):

    return await create_review(listing_id, review_data, user_id, db, background_tasks)
