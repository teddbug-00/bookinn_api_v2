from sqlalchemy import UUID
from .base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import relationship

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    name = mapped_column(String(100), nullable=True)
    date_of_birth = mapped_column(Date, nullable=True)
    phone_number = mapped_column(String(15), nullable=True)
    profile_picture_url = mapped_column(String(255), nullable=True)
    cloudinary_public_id = mapped_column(String(255), nullable=True)

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, name={self.name})>"
