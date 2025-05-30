from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import User
from app.schemas.auth import PasswordResetRequest


async def send_email(data: PasswordResetRequest, db: Session):
    if not db.query(User).where(data.email == User.email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


