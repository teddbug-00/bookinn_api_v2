from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

from src.models.property_listing import Amenities, ListingType


class ListingBase(BaseModel):
    name: str
    listing_type: ListingType
    amenities: List[Amenities] = []
    location: str
    google_maps_address: str
    price_per_night: Decimal
    room_count: int
    bathrooms_count: int
    listing_area: int
    description: str


class PropertyImageResponse(BaseModel):
    id: UUID
    image_url: str


class ListingCreateRequest(ListingBase):
    pass


class ListingCreateResponse(BaseModel):
    id: UUID
    name: str
    location: str
    price_per_night: Decimal
    room_count: int
    bathrooms_count: int
    listing_area: int
    image_thumbnail: PropertyImageResponse | None
    avg_rating: Optional[Decimal] = None
    review_count: Optional[int] = 0
    is_bookmarked: Optional[bool] = False


class ListingsListResponse(ListingCreateResponse):
    pass
