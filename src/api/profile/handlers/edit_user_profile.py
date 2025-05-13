from pickle import NONE
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models.profile import UserProfile
from src.schemas.user_profile import UserProfileUpdateRequest

async def edit_user_profile(user_id: str, update_data: Optional[UserProfileUpdateRequest], db: Session):

    if update_data is not None:

        update_dict = update_data.model_dump(exclude_none=True)

        if len(update_dict) > 0:
            try:
                curr_profile = db.get(UserProfile, user_id)
     
                if not curr_profile:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Profile not found")

                for field, value in update_dict.items():
                    if hasattr(curr_profile, field):
                        setattr(curr_profile, field, value)

                db.add(curr_profile)
                db.commit()
                db.refresh(curr_profile)
                
                return curr_profile

            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=str(e))

        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Nothing to update"
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No update request data received"
    )
        
