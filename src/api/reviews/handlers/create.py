from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.models.listing import PropertyListing
from src.models.reviews import Review
from src.schemas.review import ReviewCreateRequest

async def create_review(listing_id: str, review_data: ReviewCreateRequest, user_id: str, db: Session):
    try:
        
        listing = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()

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
            Review.listing_id == listing_id,
            Review.reviewer_id == user_id
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

        return {"message": "Review created"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )