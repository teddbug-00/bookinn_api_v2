from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.api.listing.handlers import detail
from src.models.listing import PropertyListing
from src.models.profile import UserProfile
from src.schemas.listing import ListingCreateRequest, ListingCreateResponse


async def create_listing(listing_data: ListingCreateRequest, user_id: str, db: Session) -> ListingCreateResponse:

    if not db.get(UserProfile, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        new_listing = PropertyListing(
            owner_id=user_id,
            name=listing_data.name,
            listing_type=listing_data.listing_type,
            amenities=listing_data.amenities,
            location=listing_data.location,
            google_maps_address=listing_data.google_maps_address,
            price_per_night=listing_data.price_per_night,
            room_count=listing_data.room_count,
            bathrooms_count=listing_data.bathrooms_count,
            listing_area=listing_data.listing_area,
            description=listing_data.description,
            update_popularity=True
        )

        db.add(new_listing)
        db.commit()
        db.refresh(new_listing)

        return ListingCreateResponse(
            id=new_listing.id,
            name=new_listing.name,
            image_thumbnail=new_listing.images[0] if len(new_listing.images) > 1 else None,
            location=new_listing.location,
            price_per_night=new_listing.price_per_night,
            room_count=new_listing.room_count,
            bathrooms_count=new_listing.bathrooms_count,
            listing_area=new_listing.listing_area
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
