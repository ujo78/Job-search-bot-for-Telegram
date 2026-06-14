from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from typing import Optional, Callable
import asyncio

class JobSearchScheduler:
    def __init__(self, interval_hours: int = 6):
        self.scheduler = AsyncIOScheduler()
        self.interval_hours = interval_hours
        self.search_callback = None

    def set_search_callback(self, callback: Callable):
        """Set the async callback to run on schedule."""
        self.search_callback = callback

    def add_job(self):
        """Add the scheduled job."""
        if self.search_callback:
            self.scheduler.add_job(
                self.search_callback,
                trigger=IntervalTrigger(hours=self.interval_hours),
                id='job_search',
                name='Job Search Task',
                replace_existing=True
            )

    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()

    def stop(self):
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()

    async def trigger_now(self):
        """Manually trigger search immediately."""
        if self.search_callback:
            await self.search_callback()
