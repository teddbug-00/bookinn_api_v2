from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session 

from src.api.listing.handlers.create import create_listing
from src.api.listing.handlers.delete import remove_listing
from src.api.listing.handlers.detail import fetch_full_listing_info
from src.api.listing.handlers.list import fetch_listings
from src.api.listing.handlers.reviews import fetch_reviews
from src.api.listing.handlers.update import update_listing
from src.core.db import get_db
from src.core.security import get_current_user_id
from src.schemas.listing import ListingCreateRequest, ListingCreateResponse, ListingUpdateRequest, \
    ListingUpdateResponse, ListingsListResponse
from src.schemas.review import ReviewListResponse

from typing import List

listing_router = APIRouter()


@listing_router.get("", response_model=List[ListingsListResponse], status_code=status.HTTP_200_OK)
async def get_listings(db: Session = Depends(get_db)) -> List[ListingsListResponse]:
    return await fetch_listings(db)


@listing_router.get("/{listing_id}")
async def get_listing_details(listing_id: str, db: Session = Depends(get_db)):
    return await fetch_full_listing_info(listing_id, db)


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


@listing_router.delete("/{listing_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
        listing_id: str,
        user_id: str = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    return await remove_listing(listing_id, user_id, db)