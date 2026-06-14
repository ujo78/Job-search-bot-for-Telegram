import aiosqlite
import json
from datetime import datetime
from typing import Optional, List, Dict

class JobDB:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    url_hash TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    job_description TEXT,
                    ats_type TEXT,
                    match_score REAL,
                    match_reason TEXT,
                    seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    applied_at TIMESTAMP,
                    status TEXT DEFAULT 'new'
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS resume (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    parsed_json TEXT,
                    embedding BLOB,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS pending_applies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id INTEGER NOT NULL,
                    telegram_message_id INTEGER,
                    form_screenshot_path TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(job_id) REFERENCES jobs(id)
                )
            ''')
            await db.commit()

    async def add_job(self, url: str, url_hash: str, title: str, company: str, location: str,
                      job_description: str, ats_type: Optional[str] = None) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT INTO jobs (url, url_hash, title, company, location, job_description, ats_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (url, url_hash, title, company, location, job_description, ats_type))
                await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False

    async def update_job_score(self, url_hash: str, score: float, reason: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE jobs SET match_score = ?, match_reason = ? WHERE url_hash = ?
            ''', (score, reason, url_hash))
            await db.commit()

    async def mark_applied(self, job_id: int, status: str = 'applied'):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE jobs SET applied_at = CURRENT_TIMESTAMP, status = ? WHERE id = ?
            ''', (status, job_id))
            await db.commit()

    async def get_new_jobs(self) -> List[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('''
                SELECT * FROM jobs WHERE status = 'new' ORDER BY match_score DESC LIMIT 10
            ''')
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def get_job_by_id(self, job_id: int) -> Optional[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def save_resume(self, file_path: str, parsed_json: Dict, embedding):
        async with aiosqlite.connect(self.db_path) as db:
            embedding_bytes = embedding.tobytes() if hasattr(embedding, 'tobytes') else embedding
            await db.execute('''
                DELETE FROM resume
            ''')
            await db.execute('''
                INSERT INTO resume (file_path, parsed_json, embedding)
                VALUES (?, ?, ?)
            ''', (file_path, json.dumps(parsed_json), embedding_bytes))
            await db.commit()

    async def get_resume(self) -> Optional[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM resume LIMIT 1')
            row = await cursor.fetchone()
            if row:
                return {
                    'file_path': row['file_path'],
                    'parsed_json': json.loads(row['parsed_json']),
                    'embedding': row['embedding']
                }
            return None

    async def get_applied_jobs(self, limit: int = 20) -> List[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('''
                SELECT * FROM jobs WHERE status = 'applied'
                ORDER BY applied_at DESC LIMIT ?
            ''', (limit,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
