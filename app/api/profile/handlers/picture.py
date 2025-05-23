from sqlalchemy.orm import Session
from fastapi import UploadFile

async def set_profile_picture(user_id: str, image: UploadFile, db: Session):
    """
        Implementation logic:

        First check if there is an existing profile picture.
        Remove that from both cloudinary and the database if it exists.
        Process file to maybe jpeg format to make it smaller and upload to cloudinary.
        Get the url to the profile picture, and it's id for deletion in te database
    """
    pass