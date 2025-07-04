from email.policy import HTTP
from sqlalchemy.orm import Session
from fastapi import  HTTPException, status

from app.core.security.tokens import create_access_token, create_refresh_token, verify_refresh_token
from app.models.user import User
from app.schemas.auth import TokenRefreshResponse


async def get_new_tokens(refresh_token: str, db: Session) -> TokenRefreshResponse:
    try:
        user_id = await verify_refresh_token(refresh_token)

        if user_id:
            user_exists = db.query(User).filter(User.id == user_id).first()

            if not user_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        
            access_token = await create_access_token(str(user_id))
            new_refresh_token = await create_refresh_token(str(user_id))

            return TokenRefreshResponse(
                access_token=access_token,
                refresh_token=new_refresh_token
            )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not found in token payload"
        )
        
    except Exception as e:
        raise e