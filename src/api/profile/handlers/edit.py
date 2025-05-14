from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.profile import UserProfile
from src.schemas.profiles import UserProfileUpdateRequest, UserProfileUpdateResponse


async def edit_user_profile(user_id: str, update_data: Optional[UserProfileUpdateRequest], db: Session) -> UserProfileUpdateResponse:

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
                
                return UserProfileUpdateResponse(
                    user_id=curr_profile.user_id,
                    name=curr_profile.name,
                    date_of_birth=curr_profile.date_of_birth,
                    phone_number=curr_profile.phone_number,
                    profile_picture_url=curr_profile.profile_picture_url,
                )

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
        
