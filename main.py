from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.config import settings
from src.models.base import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True)

DBSession = async_sessionmaker(engine)

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = DBSession()
    try:
        yield db
    finally:
        await db.close()

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Welcome to the API"}