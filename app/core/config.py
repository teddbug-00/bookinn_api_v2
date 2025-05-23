from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    # Database url
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Debug
    DEBUG: bool = os.getenv("DEBUG") #type: ignore

    # Password pepper
    PASSWORD_PEPPER: str = os.getenv("PASSWORD_PEPPER", "")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)  #type: ignore
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 30)  #type: ignore
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_MINUTES", 30)  #type: ignore

    # API Version
    API_VERSION: str = os.getenv("API_VERSION", "")




# A one time importable instance
settings = Settings()

print(settings.DEBUG)
print(settings.PASSWORD_PEPPER)
