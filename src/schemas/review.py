from pydantic import BaseModel, Field
from typing import Optional

class ReviewBase(BaseModel):
    rating: float = Field(default=0, ge=0, le=5, multiple_of=0.5)
    comment: str 

class ReviewCreateRequest(ReviewBase):
    pass

class ReviewUpdateRequest(BaseModel):
    rating: Optional[float] = Field(default=None, ge=0, le=5, multiple_of=0.5)
    comment: Optional[str] = None 