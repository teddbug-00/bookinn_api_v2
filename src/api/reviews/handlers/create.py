from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.listing import PropertyListing
from src.models.reviews import Review
from src.schemas.review import ReviewCreateRequest


async def _update_ratings_data(listing, db: Session, new_rating: float):

    assert listing is not None

    try:

        curr_total_ratings = float(
            (0 if listing.average_rating is None else listing.average_rating) * listing.total_reviews)

        listing.total_reviews += 1

        listing.average_rating = float((curr_total_ratings + new_rating) / listing.total_reviews).__round__(1)

        db.add(listing)
        db.commit()
        db.refresh(listing)

    except Exception as e:
        # TODO: Do proper logging here instead
        print(e)


async def create_review(listing_id: str, review_data: ReviewCreateRequest, user_id: str, db: Session):
    try:

        listing = db.query(PropertyListing).filter(listing_id == PropertyListing.id).first()

        if listing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found"
            )

        if listing.owner_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot review your own listing"
            )

        existing_review = db.query(Review).filter(
            listing_id == Review.listing_id,
            user_id == Review.reviewer_id
        ).first()

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this listing"
            )

        new_review = Review(
            listing_id=listing_id,
            reviewer_id=user_id,
            rating=review_data.rating,
            comment=review_data.comment
        )

        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        await _update_ratings_data(listing, db, review_data.rating)

        return {"message": "Review created"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
