from sqlalchemy.orm import Session

from src.models import PropertyListing


async def update_ratings(property_id: str, db: Session, new_rating: float):

    curr_property = db.get(PropertyListing, property_id)

    if curr_property:

        curr_total_ratings = float((0 if curr_property.average_rating is None else curr_property.average_rating) * curr_property.total_reviews)

        curr_property.total_reviews += 1

        curr_property.average_rating = (curr_total_ratings + new_rating) / curr_property.total_reviews

        db.add(curr_property)
        db.commit()
        db.refresh(curr_property)