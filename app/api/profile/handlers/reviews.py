from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Review
from app.models.user import User
from app.schemas.profiles import UserReviewsResponse


async def get_reviews(user_id: UUID, db: Session):

    if not db.get(User, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
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