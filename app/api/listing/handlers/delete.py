from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import PropertyListing
from app.models.profile import UserProfile
from app.logging.logger import logger


async def remove_listing(listing_id: str, user_id: str, db: Session):
    
    if not db.get(UserProfile, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    to_remove = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()

    if to_remove is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    if to_remove.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this listing"
        )

    try:
        db.delete(to_remove)
        db.commit()

    except Exception as e:
        db.rollback()
        # logger.error(f"Error deleting listing {str(to_remove.id)[:4] if to_remove is not None else ""}-******* -> {str(e)}")
        
