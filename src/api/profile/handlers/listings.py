from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.bookmarks import Bookmark
from src.models.listing import PropertyListing
from src.schemas.listing import ListingsListResponse

async def get_user_listings(user_id: str, db: Session) -> List[ListingsListResponse]:
    try:
        listings = db.query(PropertyListing).filter(user_id == PropertyListing.owner_id).all()
        
        if not listings:
            return []
        
        user_bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user_id).all()
            
        return [
            ListingsListResponse(
                id=listing.id,
                name=listing.name,
                location=listing.location,
                price_per_night=listing.price_per_night,
                room_count=listing.room_count,
                bathrooms_count=listing.bathrooms_count,
                listing_area=listing.listing_area,
                image_thumbnail=listing.images[0] if listing.images else None,
                avg_rating=0 if listing.average_rating is None else listing.average_rating,
                review_count=listing.total_reviews,
                is_bookmarked= True if listing.id in [bookmark.listing_id for bookmark in user_bookmarks] else False,
            )
            for listing in listings
        ]
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching listings: {str(e)}"
        )