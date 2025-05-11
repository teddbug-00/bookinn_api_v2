from datetime import timedelta, datetime
from typing import Optional
from jwt import JWT

from pydantic import EmailStr



def _create_token(
        user_id: EmailStr,
        token_type: str,
        expires_delta: Optional[timedelta] = None) -> None:

    expiration_date = datetime.now() + expires_delta

    payload = {
        "sub": user_id,
        "exp": expiration_date,
        "type": token_type,
    }

