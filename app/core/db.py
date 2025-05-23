from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings


engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

DBSession = sessionmaker(engine)

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
