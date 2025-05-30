from fastapi import APIRouter, BackgroundTasks, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.api.auth.handlers.refresh import get_new_tokens
from app.core.db import get_db
from app.schemas.auth import (
    LoginResponseBase,
    TokenRefreshResponse,
    UserCreateRequest,
    UserCreateResponse,
    LoginResponse,
    LoginRequest, PasswordResetRequest
)
from .handlers.login import login, login_for_swagger
from .handlers.register import register

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateRequest, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()) -> UserCreateResponse:
    return await register(user_data, db, background_tasks)


@auth_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_user(
    user_credentials: LoginRequest, 
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
    ) -> LoginResponse:

    return await login(user_credentials, db, background_tasks)


@auth_router.post("/token", response_model=LoginResponseBase, status_code=status.HTTP_200_OK)
async def login_for_swagger_ui(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> LoginResponseBase:
    return await login_for_swagger(form_data, db)


@auth_router.post("/token/refresh", response_model=TokenRefreshResponse, status_code=status.HTTP_200_OK)
async def refresh_tokens(refresh_token: str, db: Session = Depends(get_db)) -> TokenRefreshResponse:
    return await get_new_tokens(refresh_token, db)


@auth_router.post("/logout")
async def logout():
    # TODO: Complete this later.
    # Implementation logic:
    # Revoke access and refresh tokens and store revoked tokens in a redis cache
    # Before verifying tokens, check for revoked token in the cache
    pass


@auth_router.post("/password/reset")
async def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    pass

