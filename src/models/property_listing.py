import uuid

from sqlalchemy import Enum, UUID, String, DECIMAL, Integer, Text, DateTime, func, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import mapped_column, relationship

from .base import Base

class PropertyType(str, Enum):
    APARTMENT = "APARTMENT"
    GUESTHOUSE = "GUESTHOUSE"
    HOSTEL = "HOSTEL"
    HOTEL = "HOTEL"

class Amenities(str, Enum):
    INTERNET = "INTERNET"
    AC = "AC"
    SECURITY = "SECURITY"
    POWER = "POWER"


class PropertyListing(Base):
    __tablename__ = "property_listings"

    id = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    owner_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = mapped_column(String(255), index=True)
    listing_type = mapped_column(Enum(PropertyType.APARTMENT, PropertyType.GUESTHOUSE, PropertyType.HOSTEL, PropertyType.HOTEL, name="listing_type_enum"), index=True)
    amenities = mapped_column(ARRAY(Enum(Amenities.INTERNET, Amenities.AC, Amenities.SECURITY, Amenities.POWER, name="amenities_enum")), default=[])
    location = mapped_column(String(100), index=True)
    google_maps_address = mapped_column(String(500))
    latitude = mapped_column(DECIMAL(9, 6), nullable=True)
    longitude = mapped_column(DECIMAL(9, 6), nullable=True)
    price_per_night = mapped_column(DECIMAL(10, 2), index=True)
    room_count = mapped_column(Integer, default=0, index=True)
    listing_area = mapped_column(Integer, default=0)
    bathrooms_count = mapped_column(Integer, default=0)
    description = mapped_column(Text)
    is_available = mapped_column(Boolean, default=True, index=True)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="property_listings")
    images = relationship("ListingImage", back_populates="property_listing", cascade="all, delete-orphan")


class ListingImage(Base):
    __tablename__ = "listing_images"

    id = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    property_listing_id = mapped_column(UUID(as_uuid=True), ForeignKey("property_listings.id"), nullable=False)
    cloudinary_public_id = mapped_column(String(255))
    image_url = mapped_column(String(255))
    uploaded_at = mapped_column(DateTime, server_default=func.now())

    # Relationship
    property_listing = relationship("PropertyListing", back_populates="images")