from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models import User
from src.schemas.auth import LoginRequest, LoginResponse
from sqlalchemy.exc import NoResultFound

from src.utils.passwords import passwords, verify_password


async def login(user_credentials: LoginRequest, db: Session):

    try:
        user = db.query(User).filter(User.email == user_credentials.email).first()

        if not user or not verify_password(user_credentials.password, user.password_salt, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"})

        return {"message": "Login Successful"}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Incorrect email or password")