from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from src.models import PropertyListing
from src.schemas.listing import ListingsListResponse


async def fetch_listings(db: Session) -> List[ListingsListResponse]:
    try:
        # TODO: Add search filters and pagination later
        listings = db.query(PropertyListing).all()

        if not listings:
            return []

        return [ListingsListResponse(
            id=listing.id,
            name=listing.name,
            image_thumbnail=listing.images[0] if len(listing.images) > 1 else None,
            location=listing.location,
            price_per_night=listing.price_per_night,
            room_count=listing.room_count,
            bathrooms_count=listing.bathrooms_count,
            listing_area=listing.listing_area,
            avg_rating=listing.average_rating,
            review_count=listing.total_reviews,
            # TODO: Add is_bookmarked tag later in response
        ) for listing in listings]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )