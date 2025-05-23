from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.listing import PropertyListing
from app.models.profile import UserProfile
from app.schemas.listing import ListingUpdateRequest, ListingUpdateResponse


async def update_listing(listing_id: str, update_data: ListingUpdateRequest, user_id: str, db: Session) -> ListingUpdateResponse:

    if not db.get(UserProfile, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_dict = update_data.model_dump(exclude_none=True)

    if len(update_dict) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided"
        )

    try:

        curr_listing_data = db.query(PropertyListing).filter(PropertyListing.owner_id == user_id and PropertyListing.id == listing_id).first()
        
        for field, value in update_dict.items():
            if hasattr(curr_listing_data, field):
                setattr(curr_listing_data, field, value)

        db.add(curr_listing_data)
        db.commit()
        db.refresh(curr_listing_data)

        assert curr_listing_data is not None

        return ListingUpdateResponse(
            name = curr_listing_data.name,
            listing_type = curr_listing_data.listing_type,
            amenities = curr_listing_data.amenities,
            location = curr_listing_data.location,
            google_maps_address = curr_listing_data.google_maps_address,
            price_per_night = curr_listing_data.price_per_night,
            room_count = curr_listing_data.room_count,
            bathrooms_count = curr_listing_data.bathrooms_count,
            listing_area = curr_listing_data.listing_area,
            description = curr_listing_data.description
        )
            
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found for user"
        )