from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models import Review
from app.schemas.review import ReviewListResponse


async def fetch_reviews(listing_id: UUID, db: Session) -> List[ReviewListResponse]:
    try:
        reviews = db.query(Review).filter(Review.listing_id == listing_id).all()

        if not reviews:
            return []

        return [
            ReviewListResponse(
                rating=review.rating,
                comment=review.comment,
                reviewer_name=review.reviewer.name,
                reviewer_profile_picture_url=review.reviewer.profile_picture_url
            ) for review in reviews
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )