from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):

    # Database url
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")



# A one time importable instance to avoid excess initilization
settings = Settings()
