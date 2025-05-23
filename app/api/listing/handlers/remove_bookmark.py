from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.bookmarks import Bookmark
from app.models.listing import PropertyListing
from app.models.profile import UserProfile

async def remove_bookmark(db: Session, user_id: str, listing_id: str):

    if not db.get(UserProfile, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user_id , 
        Bookmark.listing_id == listing_id
    ).first()

    if not bookmark:
        return False
    
    listing = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()
    if listing:
        listing.total_bookmarks = max(0, listing.total_bookmarks - 1)
        listing.update_popularity = True

    db.delete(bookmark)
    db.commit()
    return True