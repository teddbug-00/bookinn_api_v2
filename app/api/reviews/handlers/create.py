from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import DBSession
from app.models.activities import Activity, ActivityAction, ActivityType
from app.models.listing import PropertyListing
from app.models.reviews import Review
from app.models.user import User
from app.schemas.review import ReviewCreateRequest
from app.logging.logger import logger


async def _update_ratings_data(listing_id: str, user_id: str, new_rating: float):

    db = DBSession()

    listing = None

    try:
        listing = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()

        if listing is not None:

            curr_total_ratings = float(listing.average_rating * listing.total_reviews)

            listing.total_reviews += 1

            listing.average_rating = float((curr_total_ratings + float(new_rating)) / listing.total_reviews).__round__(1)

            print(listing.average_rating)


            listing.update_popularity = True

            db.add(listing)
            db.commit()

    except Exception as e:
        if listing is not None:
            logger.error(
                f"Error updating rating data for listing {str(listing.id)[:4]}-*******: {str(e)}"
            )

    if listing is not None:
        await _save_activity(listing, user_id, db)


async def _save_activity(listing: PropertyListing, user_id: str, db: Session):
    
    try:
        reviewer_activity = Activity(
            user_id=user_id,
            type=ActivityType.REVIEW,
            action=ActivityAction.CREATE,
            entity_id=listing.id,
            entity_type="PropertyListing",
            metadatas={
                "listing_id": str(listing.id),
                "listing_name": listing.name,
                "listing_image_thumbnail": listing.images[0] if len(listing.images) > 0 else None
            }
        )


        listing_owner_activity = Activity(
            user_id=listing.owner_id,
            type=ActivityType.REVIEW,
            action=ActivityAction.RECEIVE,
            entity_id=listing.id,
            entity_type="PropertyListing",
            metadatas={
                "listing_id": str(listing.id),
                "listing_name": listing.name,
                "listing_image_thumbnail": listing.images[0] if len(listing.images) > 0 else None
            }
        )

        db.add_all([reviewer_activity, listing_owner_activity])
        db.commit()
    
    except Exception as e:
        logger.error(
            f"Error saving activity data for users {str(user_id)[:4]}-******** and {str(listing.owner_id)[:4]}-********: {str(e)}"
        )


async def create_review(
        listing_id: str, 
        review_data: ReviewCreateRequest, 
        user_id: str, 
        db: Session, 
        background_tasks: BackgroundTasks):

    if not db.get(User, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) 
    
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have already reviewed this listing"
        )
    
    try:
        new_review = Review(
            listing_id=listing_id,
            reviewer_id=user_id,
            rating=review_data.rating,
            comment=review_data.comment
        )

        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        background_tasks.add_task(
            _update_ratings_data,
            listing_id,
            user_id,
            new_review.rating,
        )

        return {"message": "Review created"}

    except Exception as e:
        
        logger.error(
            f"Error creating review: {str(e)}"
        )
