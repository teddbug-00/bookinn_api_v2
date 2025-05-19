from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.schemas.auth import LoginResponseBase, UserCreateRequest, UserCreateResponse, LoginResponse, LoginRequest
from .handlers.login import login, login_for_swagger
from .handlers.register import register

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateRequest, db: Session = Depends(get_db)) -> UserCreateResponse:
    return await register(user_data, db)


@auth_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_user(user_credentials: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    return await login(user_credentials, db)


@auth_router.post("/token", response_model=LoginResponseBase, status_code=status.HTTP_200_OK)
async def login_for_swagger_ui(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> LoginResponseBase:
    return await login_for_swagger(form_data, db)


@auth_router.post("/logout")
async def logout():
    # TODO: Complete this later.
    # Implementation logic:
    # Revoke access and refresh tokens and store revoked tokens in a redis cache
    # Before verifying tokens, check for revoked token in the cache
    pass


