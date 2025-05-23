from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, DateTime, UniqueConstraint, func
import uuid

from .base import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"
    __table_args__ = (
        UniqueConstraint('user_id', 'listing_id', name='unique_user_listing_bookmark'),
    )

    id = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    listing_id = mapped_column(UUID(as_uuid=True), ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    added_on = mapped_column(DateTime, server_default=func.now())

    user = relationship(
        "User", 
        back_populates="bookmarks",
        overlaps="bookmarked_by,bookmarked_listings"
    )
    listing = relationship(
        "PropertyListing", 
        back_populates="bookmarks",
        overlaps="bookmarked_by,bookmarked_listings")
