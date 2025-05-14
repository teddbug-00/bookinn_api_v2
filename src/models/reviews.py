import uuid

from sqlalchemy import UUID, DateTime, ForeignKey, Text, func, DECIMAL
from sqlalchemy.orm import mapped_column, relationship

from .base import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    listing_id = mapped_column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    reviewer_id = mapped_column(UUID(as_uuid=True), ForeignKey("user_profiles.user_id"), nullable=False)
    rating = mapped_column(DECIMAL, nullable=False)
    comment = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    listing = relationship("PropertyListing", back_populates="reviews")
    reviewer = relationship("UserProfile", back_populates="reviews")
