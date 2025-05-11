from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    name: str
    date_of_birth: date
    phone_number: str

    # @field_validator("password_confirm")
    # def passwords_match(cls, v, values):
    #     if "password" in values and v != values["password"]:
    #         raise ValueError("Passwords don't match")
    #     return v


class UserResponse(BaseModel):
    user_id: str
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
    user_id: str


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

    # @field_validator("password_confirm")
    # def passwords_match(cls, v, values):
    #     if "password" in values and v != values["password"]:
    #         raise ValueError("Passwords don't match")
    #     return v