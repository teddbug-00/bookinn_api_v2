from sqlalchemy.orm import Session

from src.models.bookmarks import Bookmark
from src.models.listing import PropertyListing

async def remove_bookmark(db: Session, user_id: str, listing_id: str):

    bookmark = db.query(Bookmark).filter(
        user_id == Bookmark.user_id, 
        listing_id == Bookmark.listing_id
    ).first()

    if not bookmark:
        return False
    
    listing = db.query(PropertyListing).filter(listing_id == PropertyListing.id).first()
    if listing:
        listing.total_bookmarks = max(0, listing.total_bookmarks - 1)
        listing.update_popularity = True

    db.delete(bookmark)
    db.commit()
    return True