from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.security import create_access_token, create_refresh_token
from src.models import User
from src.schemas.auth import LoginRequest, LoginResponse
from sqlalchemy.exc import NoResultFound

from src.utils.passwords import verify_password


async def login(user_credentials: LoginRequest, db: Session) -> LoginResponse:

    try:

        user = db.query(User).filter(user_credentials.email == User.email).first()

        if not user or not verify_password(user_credentials.password, user.password_salt, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"})

        access_token = await create_access_token(str(user.id))
        refresh_token = await create_refresh_token(str(user.id))

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_id=user.id
        )

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Incorrect email or password")



async def login_for_swagger(form_data: OAuth2PasswordRequestForm, db: Session) -> LoginResponse:
    try:
        user = db.query(User).filter(form_data.username == User.email).first()

        if not user or not verify_password(form_data.password, user.password_salt, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"})

        access_token = await create_access_token(str(user.id))
        refresh_token = await create_refresh_token(str(user.id))

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_id=user.id
        )

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Incorrect email or password")