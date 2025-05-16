from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models import PropertyListing
from src.schemas.listing import ListingDetailsResponse, ListingImageResponse


async def fetch_full_listing_info(listing_id: str, db: Session) -> ListingDetailsResponse:
    try:
        listing = db.get(PropertyListing, listing_id)

        # TODO: why does the except block take precedence over this?
        if listing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found",
            )

        return ListingDetailsResponse(
            name=listing.name,
            owner_id=str(listing.owner_id),
            owner_name=listing.owner.profile.name,
            listing_type=listing.listing_type,
            amenities=listing.amenities,
            is_available=listing.is_available,
            location=listing.location,
            google_maps_address=listing.google_maps_address,
            price_per_night=listing.price_per_night,
            room_count=listing.room_count,
            listing_area=listing.listing_area,
            bathrooms_count=listing.bathrooms_count,
            images=[
                ListingImageResponse(
                    id=image.id,
                    image_url=image.image_url,
                )
                for image in listing.images
            ] if listing.images else [],
            average_rating=listing.average_rating,
            review_count=listing.total_reviews,
            # TODO: Add is_bookmarked later
            description=listing.description
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
