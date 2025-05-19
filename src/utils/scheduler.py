from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.core.db import DBSession
from src.utils.tasks import update_popularity_scores
from contextlib import asynccontextmanager

def setup_scheduler(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        update_popularity_scores,
        CronTrigger(second=59),
        # CronTrigger(hour='*/6')
        args=[DBSession()],
        kwargs={'batch_size': 100},
        id='update_popularity_scores',
        replace_existing=True
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        scheduler.start()
        print("Scheduler cron started")
        try:
            yield
        finally:
            scheduler.shutdown()
            print("Scheduler cron stopped")

    app.router.lifespan_context = lifespan
