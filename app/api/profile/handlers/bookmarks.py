from sqlalchemy.orm import Session
from typing import List

from app.models.bookmarks import Bookmark
from app.schemas.bookmarks import BookmarksListResponse

async def fetch_user_bookmarks(user_id: str, db: Session) -> List[BookmarksListResponse]:
    try:
        bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user_id).all()

        if not bookmarks:
            return []
        
        return [BookmarksListResponse(
            id = bookmark.listing_id,
            name = bookmark.listing.name,
            location = bookmark.listing.location,
            price_per_night = bookmark.listing.price_per_night,
            room_count = bookmark.listing.room_count,
            bathrooms_count = bookmark.listing.bathrooms_count,
            listing_area = bookmark.listing.listing_area,
            image_thumbnail = bookmark.listing.images[0] if bookmark.listing.images else None,
            avg_rating = 0 if bookmark.listing.average_rating is None else bookmark.listing.average_rating,
            review_count = bookmark.listing.total_reviews,
            is_bookmarked = True  # True always
        ) for bookmark in bookmarks]

    except Exception as e:
        raise e