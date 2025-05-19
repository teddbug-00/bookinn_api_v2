from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.bookmarks import Bookmark
from src.models.listing import PropertyListing

async def add_bookmark(user_id: str, listing_id: str, db: Session):
    try:
        bookmark = Bookmark(
            user_id=user_id,
            listing_id=listing_id
        )

        db.add(bookmark)

        listing = db.query(PropertyListing).filter(bookmark.listing_id == PropertyListing.id).first()
        if listing:
            listing.total_bookmarks += 1

        db.commit()
        db.refresh(bookmark)

        return {"status": "Bookmark added"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listing already bookmarked"
        )

