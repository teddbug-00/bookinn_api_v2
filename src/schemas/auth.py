from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    name: str
    date_of_birth: date
    phone_number: str


class UserCreateResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    name: str
    date_of_birth: str
    phone_number: str
    profile_picture_url: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: UUID


class TokenRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginForm(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    password: str
    password_confirm: str
