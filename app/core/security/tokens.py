from datetime import UTC, timedelta, datetime
from typing import Optional
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer

from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWEInvalidAuth
from fastapi import WebSocket, WebSocketException, status, HTTPException, Depends
from pydantic import BaseModel

from app.core.config import settings


api_version_str = f"/api/{settings.API_VERSION}"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{api_version_str}/auth/token")

class TokenPayload(BaseModel):
    sub: UUID
    exp: datetime
    type: str


async def _create_token(user_id: str, token_type: str, expires_delta: Optional[timedelta] = None) -> str:

    default_expires = {
        "access": timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "refresh": timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        "password_reset": timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    }

    payload = {
        "sub": user_id,
        "exp": datetime.now() + (expires_delta or default_expires[token_type]),
        "type": token_type
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


async def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    return await _create_token(user_id, "access", expires_delta)


async def verify_refresh_token(token: str) -> str:

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    token_data = TokenPayload(**payload)

    if token_data.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type"
        )
        
    if datetime.now(UTC) > token_data.exp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token expired"
        )
        
    return str(token_data.sub)



async def verify_access_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        token_data = TokenPayload(**payload)

        if token_data.type != "access":
            return False
        
        return True
    
    except Exception:
        return False


async def create_refresh_token(user_id:str, expires_delta: Optional[timedelta] = None) -> str:
    return await _create_token(user_id, "refresh", expires_delta)


async def _decode_token(token: str, add_auth_header: bool =True) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        token_data = TokenPayload(**payload)

        return token_data

    except JWEInvalidAuth:
        headers = {"WWW-Authenticate": "Bearer"} if add_auth_header else {}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers=headers,
        )
    except ExpiredSignatureError:
        headers = {"WWW-Authenticate": "Bearer"} if add_auth_header else {}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature expired",
            headers=headers
        )
    except JWTError:
        headers = {"WWW-Authenticate": "Bearer"} if add_auth_header else {}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers=headers
        )


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:

    payload = await _decode_token(token, add_auth_header=True)

    if payload.type != "access":
        headers = {"WWW-Authenticate": "Bearer"}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type for authentication",
            headers=headers
        )

    if payload.sub is None:
        headers = {"WWW-Authenticate": "Bearer"}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers=headers
        )

    return payload.sub


async def get_current_user_ws(websocket: WebSocket):
    print("Get websocket called")
    try:
        token = websocket.query_params.get("token")
        if token is not None:
            payload = await _decode_token(token, add_auth_header=True)
            
            if payload.sub is None:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return payload.sub
    except:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    