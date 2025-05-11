from datetime import timedelta, datetime
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWEInvalidAuth
from fastapi import status, HTTPException, Depends

from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def _create_token(user_id: str, token_type: str, expires_delta: Optional[timedelta] = None) -> str:

    default_expires = {
        "access": timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "refresh": timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        "password_reset": timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    }

    expire = datetime.now() + (expires_delta or default_expires[token_type])

    payload = {
        "sub": user_id,
        "exp": expire,
        "type": token_type
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


async def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    return await _create_token(user_id, "access", expires_delta)


async def create_refresh_token(user_id:str, expires_delta: Optional[timedelta] = None) -> str:
    return await _create_token(user_id, "refresh", expires_delta)

async def _decode_token(token: str, add_auth_header: bool =True) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")

        if user_id is None:
            headers = {"WWW-Authenticate": "Bearer"} if add_auth_header else {}
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers=headers
            )

        return user_id

    except JWEInvalidAuth:
        headers = {"WWW-Authenticate": "Bearer"} if add_auth_header else {}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers=headers,
        )

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    return await _decode_token(token, add_auth_header=True)
