from sqlalchemy.orm import Session

from src.models.property_listing import PropertyListing
from src.schemas.listing import ListingsListResponse

async def get_user_listings(user_id: str, db: Session):
    # TODO: Not so complete yet. At least I got the basic setup working, hehe
    if user_id:
        try:
            listings = db.query(PropertyListing).filter(PropertyListing.owner_id == user_id).all()
            print(listings)
        except Exception as e:
            print(e)