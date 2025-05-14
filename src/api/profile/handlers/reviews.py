from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models import Review
from src.schemas.profiles import UserReviewsResponse


async def get_reviews(user_id: UUID, db: Session):
    try:

        reviews = db.query(Review).filter(user_id == Review.reviewer_id).all()

        if not reviews:
            return []

        return [
            UserReviewsResponse(
                review_id=review.id,
                rating=review.rating,
                comment=review.comment
            )
            for review in reviews
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )