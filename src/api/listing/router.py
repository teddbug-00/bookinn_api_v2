from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session 

from src.api.listing.handlers.create import create_listing
from src.api.listing.handlers.reviews import fetch_reviews
from src.api.listing.handlers.update import update_listing
from src.core.db import get_db
from src.core.security import get_current_user_id
from src.schemas.listing import ListingCreateRequest, ListingCreateResponse, ListingUpdateRequest, ListingUpdateResponse
from src.schemas.review import ReviewListResponse

from typing import List

listing_router = APIRouter()


@listing_router.post("/add", response_model=ListingCreateResponse, status_code=status.HTTP_201_CREATED)
async def add_listing(
    listing_data: ListingCreateRequest, 
    user_id: str = Depends(get_current_user_id), 
    db: Session = Depends(get_db)) -> ListingCreateResponse | None:

    return await create_listing(listing_data, user_id, db)


@listing_router.get("/{listing_id}/reviews", response_model=List[ReviewListResponse], status_code=status.HTTP_200_OK)
async def get_reviews(
        listing_id: UUID,
        db: Session = Depends(get_db)) -> List[ReviewListResponse]:
    return await fetch_reviews(listing_id, db)


@listing_router.patch("/{listing_id}/update", response_model=ListingUpdateResponse, status_code=status.HTTP_200_OK)
async def edit_listing(
    listing_id: str,
    update_data: ListingUpdateRequest, 
    user_id: str = Depends(get_current_user_id), 
    db: Session = Depends(get_db)) -> ListingUpdateResponse:

    return await update_listing(listing_id, update_data, user_id, db)
