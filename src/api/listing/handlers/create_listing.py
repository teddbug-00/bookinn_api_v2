from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.property_listing import PropertyListing
from src.schemas.listing import ListingCreateRequest, ListingCreateResponse


async def create_listing(listing_data: ListingCreateRequest, user_id: str, db: Session) -> ListingCreateResponse | None:
    if user_id:
        try:
            new_listing = PropertyListing(
                owner_id = user_id,
                name = listing_data.name,
                listing_type = listing_data.listing_type,
                amenities = listing_data.amenities,
                location = listing_data.location,
                google_maps_address = listing_data.google_maps_address,
                price_per_night = listing_data.price_per_night,
                room_count = listing_data.room_count,
                bathrooms_count = listing_data.bathrooms_count,
                listing_area = listing_data.listing_area,
                description = listing_data.description
            )

            db.add(new_listing)
            db.commit()
            db.refresh(new_listing)

            return ListingCreateResponse(
                id = new_listing.id,
                name = new_listing.name,
                image_thumbnail = new_listing.images[0] if len(new_listing.images) > 1 else None,
                location = new_listing.location,
                price_per_night = new_listing.price_per_night,
                room_count = new_listing.room_count,
                bathrooms_count = new_listing.bathrooms_count,
                listing_area = new_listing.listing_area
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f"Faled to add property. Error: {str(e)}"
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized"
    )