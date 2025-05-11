from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session 

from src.api.listing.handlers.create_listing import create_listing
from src.core.db import get_db
from src.core.security import get_current_user_id
from src.schemas.listing import ListingCreateRequest, ListingCreateResponse

listing_router = APIRouter()

@listing_router.post("/add", response_model=ListingCreateResponse, status_code=status.HTTP_201_CREATED)
async def add_listing(
    listing_data: ListingCreateRequest, 
    user_id: str = Depends(get_current_user_id), 
    db: Session = Depends(get_db)) -> ListingCreateResponse | None:

    return await create_listing(listing_data, user_id, db)