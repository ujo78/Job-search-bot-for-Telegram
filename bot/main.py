import asyncio
import logging
from aiogram import Dispatcher, Bot, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import TELEGRAM_BOT_TOKEN, SEARCH_INTERVAL_HOURS, SEARCH_KEYWORDS, LOCATION, COUNTRY, ANTHROPIC_API_KEY, ADZUNA_APP_ID, ADZUNA_API_KEY
from bot.handlers import router as handlers_router
from bot.scheduler import JobSearchScheduler
from storage.db import JobDB
from scraper.jobspy_scraper import scrape_jobspy
from scraper.free_apis import fetch_remoteok, fetch_adzuna, fetch_jobicy
from scraper.aggregator import aggregate_jobs
from matcher.embedder import JobEmbedder
from matcher.llm_ranker import LLMRanker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobSearchBot:
    def __init__(self, token: str, search_interval: int):
        self.bot = Bot(token=token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.scheduler = JobSearchScheduler(interval_hours=search_interval)
        self.db = JobDB("job_search.db")
        self.embedder = JobEmbedder()
        self.llm_ranker = LLMRanker(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

    async def initialize(self):
        """Initialize bot and database."""
        await self.db.init()

        # Register handlers
        self.dp.include_router(handlers_router)

        # Set up scheduled job
        self.scheduler.set_search_callback(self.search_and_notify)
        self.scheduler.add_job()

        # Set bot commands
        commands = [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="resume", description="Upload your resume"),
            BotCommand(command="search", description="Search for jobs"),
            BotCommand(command="status", description="Check status"),
            BotCommand(command="history", description="View application history"),
        ]
        await self.bot.set_my_commands(commands)

    async def search_and_notify(self):
        """Main job search pipeline."""
        try:
            logger.info("Starting job search...")

            # Get resume and embedding
            resume_data = await self.db.get_resume()
            if not resume_data:
                logger.warning("No resume found, skipping search")
                return

            resume_embedding = resume_data['embedding']
            if isinstance(resume_embedding, bytes):
                import numpy as np
                resume_embedding = np.frombuffer(resume_embedding, dtype=np.float32)

            # Scrape jobs from all sources
            jobspy_jobs = await scrape_jobspy(
                search_term=SEARCH_KEYWORDS,
                location=LOCATION,
                country=COUNTRY,
                max_results=30
            )

            remoteok_jobs = await fetch_remoteok(max_results=10)
            adzuna_jobs = await fetch_adzuna(ADZUNA_APP_ID, ADZUNA_API_KEY, max_results=10)
            jobicy_jobs = await fetch_jobicy(max_results=10)

            # Aggregate
            all_jobs = [jobspy_jobs, remoteok_jobs, adzuna_jobs, jobicy_jobs]
            aggregated = await aggregate_jobs(all_jobs)

            logger.info(f"Found {len(aggregated)} jobs after dedup")

            # Score with embeddings
            top_jobs = self.embedder.rank_jobs(resume_embedding, aggregated, top_n=50)

            # Score with LLM if available
            if self.llm_ranker:
                resume_text = resume_data['parsed_json'].get('full_text', '')[:2000]
                llm_scores = self.llm_ranker.score_jobs(resume_text, [job for job, _ in top_jobs])

                for llm_score in llm_scores:
                    idx = llm_score.get('index', 1) - 1
                    if idx < len(top_jobs):
                        job, _ = top_jobs[idx]
                        await self.db.update_job_score(
                            job['url_hash'],
                            llm_score.get('score', 5),
                            llm_score.get('reason', '')
                        )

            # Add to DB
            for job, score in top_jobs:
                await self.db.add_job(
                    url=job['url'],
                    url_hash=job['url_hash'],
                    title=job['title'],
                    company=job['company'],
                    location=job['location'],
                    job_description=job.get('job_description', ''),
                    ats_type=job.get('ats_type', 'unknown')
                )

            logger.info(f"Processed {len(top_jobs)} jobs")

        except Exception as e:
            logger.error(f"Search error: {e}")

    async def start(self, user_id: int):
        """Start the bot."""
        await self.initialize()
        self.scheduler.start()

        logger.info("Bot started, polling for updates...")

        # Start polling
        await self.dp.start_polling(self.bot)

    async def stop(self):
        """Stop the bot."""
        self.scheduler.stop()
        await self.bot.session.close()

async def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")

    bot = JobSearchBot(TELEGRAM_BOT_TOKEN, SEARCH_INTERVAL_HOURS)
    await bot.start(user_id=0)

if __name__ == "__main__":
    asyncio.run(main())
