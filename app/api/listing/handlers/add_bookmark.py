from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.bookmarks import Bookmark
from app.models.listing import PropertyListing
from app.models.profile import UserProfile

async def add_bookmark(user_id: str, listing_id: str, db: Session):

    if not db.get(UserProfile, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        bookmark = Bookmark(
            user_id=user_id,
            listing_id=listing_id
        )

        db.add(bookmark)

        listing = db.query(PropertyListing).filter(listing_id == PropertyListing.id).first()
        if listing:
            listing.total_bookmarks += 1
            listing.update_popularity = True

        db.commit()
        
        return {"status": "Bookmark added"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listing already bookmarked"
        )

