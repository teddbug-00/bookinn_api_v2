from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.listing import PropertyListing
from app.utils.popularity_algo import calculate_popularity_score

async def update_popularity_scores(db: Session, batch_size: int = 100):
    """
    Asynchronously updates the popularity scores for PropertyListing records in the database in batches.
    Args:
        db (Session): SQLAlchemy database session used for querying and updating records.
        batch_size (int, optional): Number of records to process in each batch. Defaults to 100.
    Process:
        - Retrieves PropertyListing records ordered by most recently updated and only those tagged for update.
        - For each batch, calculates and updates the popularity_score for each listing.
        - Commits the changes to the database after processing each batch and changes the to_update tag.
        - Continues processing until all listings have been updated.
    """
    offset = 0
    while True:
        listings = db.query(PropertyListing)\
            .filter(PropertyListing.update_popularity == True)\
            .order_by(desc(PropertyListing.updated_at))\
            .offset(offset)\
            .limit(batch_size)\
            .all()
        
        if not listings:
            break
            
        for listing in listings:
            listing.popularity_score = calculate_popularity_score(listing)
            listing.update_popularity = False
            
        db.bulk_save_objects(listings)
        db.commit()
        
        offset += batch_size
        