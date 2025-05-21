from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from src.models.activities import Activity
from src.models.user import User
from src.logging.logger import logger
from src.schemas.profiles import UserActivitiesResponse

async def fetch_user_activities(user_id: UUID, db: Session) -> List[UserActivitiesResponse]:
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        activities = db.query(Activity).filter(Activity.user_id == user_id).all()

        if not activities:
            return []
        
        return [
            UserActivitiesResponse(
                type=activity.type,
                action=activity.action,
                entity_type=activity.entity_type,
                metadata=activity.metadatas,
                created_at=activity.created_at
            ) for activity in activities
        ]
    
    except Exception as e:
        logger.error(f"Error fetching activies for user {str(user_id)[:4]}-******* {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
