from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    # Database url
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Password pepper
    PASSWORD_PEPPER: str = os.getenv("PASSWORD_PEPPER", "")



# A one time importable instance to avoid excess initialization
settings = Settings()
