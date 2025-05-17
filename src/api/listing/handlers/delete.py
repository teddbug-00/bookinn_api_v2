from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models import PropertyListing


async def remove_listing(listing_id: str, user_id: str, db: Session):
    try:

        to_remove = db.query(PropertyListing).filter(listing_id == PropertyListing.id).first()

        if not to_remove:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found"
            )

        if to_remove.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        db.delete(to_remove)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
