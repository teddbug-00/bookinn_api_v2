from decimal import Decimal
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from uuid import UUID

class ListingType(str, Enum):
    APARTMENT = "APARTMENT"
    GUESTHOUSE = "GUESTHOUSE"
    HOSTEL = "HOSTEL"
    HOTEL = "HOTEL"


class Amenities(str, Enum):
    INTERNET = "INTERNET"
    AC = "AC"
    SECURITY = "SECURITY"
    POWER = "POWER"


class ListingBase(BaseModel):
    name: str
    listing_type: ListingType
    amenities: List[Amenities]
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

class ListingUpdateRequest(BaseModel):
    name: Optional[str] = None
    listing_type: Optional[ListingType] = None
    amenities: Optional[List[Amenities]] = None
    location: Optional[str] = None
    google_maps_address: Optional[str] = None
    price_per_night: Optional[Decimal] = None
    room_count: Optional[int] = None
    bathrooms_count: Optional[int] = None
    listing_area: Optional[int] = None
    description: Optional[str] = None


class ListingUpdateResponse(ListingBase):
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


class ListingDetailsResponse(ListingBase):
    # TODO: Complete this later
    pass
