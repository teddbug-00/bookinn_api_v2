from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.db import DBSession
from app.core.config import settings
from app.utils.tasks import update_popularity_scores
from contextlib import asynccontextmanager

def setup_scheduler(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        update_popularity_scores,
        CronTrigger(hour='*/6') if not settings.DEBUG else CronTrigger(second=30),
        args=[DBSession()],
        kwargs={'batch_size': 100},
        id='update_popularity_scores',
        replace_existing=True
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        scheduler.start()
        try:
            yield
        finally:
            scheduler.shutdown()

    app.router.lifespan_context = lifespan
