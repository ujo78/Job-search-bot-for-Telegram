from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
import numpy as np

from config import RESUME_DIR, SCREENSHOTS_DIR, SEARCH_KEYWORDS, LOCATION, COUNTRY, ANTHROPIC_API_KEY, ADZUNA_APP_ID, ADZUNA_API_KEY
from bot.keyboards import main_menu, job_digest_keyboard, apply_confirmation_keyboard
from matcher.resume_parser import parse_resume
from matcher.embedder import JobEmbedder
from matcher.llm_ranker import LLMRanker
from storage.db import JobDB
from scraper.jobspy_scraper import scrape_jobspy
from scraper.free_apis import fetch_remoteok, fetch_adzuna, fetch_jobicy
from scraper.aggregator import aggregate_jobs
from applier.apply_session import ApplySession

router = Router()

class ResumeUpload(StatesGroup):
    waiting_for_resume = State()

class ApplyFlow(StatesGroup):
    waiting_for_confirmation = State()
    job_id = State()
    session_id = State()

async def init_db():
    """Initialize database."""
    db = JobDB("job_search.db")
    await db.init()
    return db

# Store active apply sessions temporarily
active_sessions = {}

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Start command."""
    await message.answer(
        "👋 Welcome to Job Search Bot!\n\n"
        "I'll help you find and apply to jobs that match your resume.\n\n"
        "Commands:\n"
        "/resume - Upload your PDF resume\n"
        "/search - Search for matching jobs\n"
        "/status - Check today's activity\n"
        "/history - View applied jobs\n",
        reply_markup=main_menu()
    )

@router.message(Command("resume"))
async def cmd_resume(message: types.Message, state: FSMContext):
    """Resume upload command."""
    await message.answer("📄 Please upload your PDF resume:")
    await state.set_state(ResumeUpload.waiting_for_resume)

@router.message(ResumeUpload.waiting_for_resume, F.document)
async def process_resume(message: types.Message, state: FSMContext):
    """Process resume upload."""
    if not message.document.file_name.lower().endswith('.pdf'):
        await message.answer("❌ Please upload a PDF file.")
        return

    try:
        file = await message.bot.get_file(message.document.file_id)
        file_path = os.path.join(RESUME_DIR, message.document.file_name)

        await message.bot.download_file(file.file_path, file_path)

        # Parse resume
        resume_data = parse_resume(file_path)
        db = await init_db()

        # Compute embedding
        embedder = JobEmbedder()
        embedding = embedder.resume_embedding(resume_data['full_text'])

        # Save to DB
        await db.save_resume(file_path, resume_data, embedding)

        await message.answer(
            f"✅ Resume uploaded successfully!\n\n"
            f"Skills detected: {len(resume_data['skills'])}\n"
            f"Experience entries: {len(resume_data['experience'])}\n"
            f"Education entries: {len(resume_data['education'])}\n\n"
            f"Ready to search for jobs!",
            reply_markup=main_menu()
        )

        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Error: {str(e)}")
        await state.clear()

@router.message(Command("search"))
async def cmd_search(message: types.Message):
    """Search for jobs using full pipeline."""
    await message.answer("🔍 Searching for matching jobs...\n(This may take 30-60 seconds)")

    try:
        db = await init_db()

        # Get resume and embedding
        resume_data = await db.get_resume()
        if not resume_data:
            await message.answer("❌ No resume found. Upload with /resume first.")
            return

        # Restore embedding from bytes
        embedding_bytes = resume_data['embedding']
        if isinstance(embedding_bytes, bytes):
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        else:
            embedding = resume_data['embedding']

        resume_text = resume_data['parsed_json'].get('full_text', '')

        # Scrape jobs from all sources
        jobspy_jobs = await scrape_jobspy(
            search_term=SEARCH_KEYWORDS,
            location=LOCATION,
            country=COUNTRY,
            max_results=20
        )

        remoteok_jobs = await fetch_remoteok(max_results=5)
        adzuna_jobs = await fetch_adzuna(ADZUNA_APP_ID, ADZUNA_API_KEY, what=SEARCH_KEYWORDS, max_results=5)
        jobicy_jobs = await fetch_jobicy(max_results=5)

        # Aggregate
        all_jobs = [jobspy_jobs, remoteok_jobs, adzuna_jobs, jobicy_jobs]
        aggregated = await aggregate_jobs(all_jobs)

        if not aggregated:
            await message.answer("❌ No jobs found. Try different search keywords.")
            return

        # Score with embeddings
        embedder = JobEmbedder()
        top_jobs = embedder.rank_jobs(embedding, aggregated, top_n=15)

        # Score with LLM if available
        if ANTHROPIC_API_KEY:
            llm_ranker = LLMRanker(api_key=ANTHROPIC_API_KEY)
            llm_scores = llm_ranker.score_jobs(resume_text[:2000], [job for job, _ in top_jobs])

            for llm_score in llm_scores:
                idx = llm_score.get('index', 1) - 1
                if idx < len(top_jobs):
                    job, _ = top_jobs[idx]
                    await db.update_job_score(
                        job['url_hash'],
                        llm_score.get('score', 5),
                        llm_score.get('reason', '')
                    )

        # Add to DB
        for job, score in top_jobs:
            await db.add_job(
                url=job['url'],
                url_hash=job['url_hash'],
                title=job['title'],
                company=job['company'],
                location=job['location'],
                job_description=job.get('job_description', ''),
                ats_type=job.get('ats_type', 'unknown')
            )

        # Display results
        result_text = f"Found {len(aggregated)} jobs ({len(top_jobs)} shown after ranking):\n\n"

        for i, (job, score) in enumerate(top_jobs[:10], 1):
            title = job.get('title', 'Unknown')[:30]
            company = job.get('company', 'Unknown')[:20]
            location = job.get('location', 'Remote')[:15]
            reason = job.get('match_reason', 'Good fit')[:40]

            result_text += f"{i}. {title} @ {company}\n"
            result_text += f"   Location: {location}\n"
            result_text += f"   Fit: {reason}\n\n"

        await message.answer(result_text)

        # Send first job with apply button
        if top_jobs:
            first_job, first_score = top_jobs[0]
            msg_text = f"Top match:\n\n<b>{first_job['title']}</b>\n"
            msg_text += f"Company: {first_job['company']}\n"
            msg_text += f"Location: {first_job['location']}\n"
            msg_text += f"Match: {first_job.get('match_reason', 'Good fit')}\n\n"
            msg_text += f"<a href='{first_job['url']}'>View Job</a>"

            sent_msg = await message.answer(msg_text, parse_mode="HTML", reply_markup=job_digest_keyboard())

            # Store job data for apply callback
            active_sessions[sent_msg.message_id] = {
                'job': first_job,
                'user_id': message.from_user.id
            }

    except Exception as e:
        await message.answer(f"❌ Search error: {str(e)[:100]}")

@router.message(Command("status"))
async def cmd_status(message: types.Message):
    """Show status."""
    db = await init_db()
    new_jobs = await db.get_new_jobs()

    await message.answer(
        f"📊 Job Search Status\n\n"
        f"New jobs found today: {len(new_jobs)}\n"
        f"Jobs reviewed: 0\n"
        f"Applications sent: 0\n",
        reply_markup=main_menu()
    )

@router.message(Command("history"))
async def cmd_history(message: types.Message):
    """Show application history."""
    db = await init_db()
    applied_jobs = await db.get_applied_jobs(limit=10)

    if not applied_jobs:
        await message.answer("📋 No applications yet.", reply_markup=main_menu())
        return

    history_text = "📋 Application History\n\n"
    for i, job in enumerate(applied_jobs, 1):
        history_text += f"{i}. {job['title']} at {job['company']}\n"

    await message.answer(history_text, reply_markup=main_menu())

@router.callback_query(F.data == "apply")
async def handle_apply(query: types.CallbackQuery, state: FSMContext):
    """Handle apply button - prepare form preview."""
    try:
        # Get the job from active sessions
        msg_id = query.message.message_id
        session_data = active_sessions.get(msg_id)

        if not session_data:
            await query.answer("❌ Job session expired", show_alert=True)
            return

        job = session_data['job']
        await query.answer("📝 Preparing form preview...", show_alert=False)
        await query.message.edit_text(f"⏳ Loading form for {job['title']} at {job['company']}...")

        # Get user info and resume
        db = await init_db()
        resume_data = await db.get_resume()

        if not resume_data:
            await query.message.edit_text("❌ No resume found")
            return

        resume_text = resume_data['parsed_json'].get('full_text', '')

        # Create apply session
        user_info = {
            'full_name': 'Job Applicant',
            'first_name': 'Job',
            'last_name': 'Applicant',
            'email': 'applicant@example.com',
            'phone': '+1-555-0000',
            'resume_path': resume_data['file_path']
        }

        apply_session = ApplySession(job, resume_text, user_info, db, SCREENSHOTS_DIR)

        # Prepare preview (take screenshot)
        screenshot_path = await apply_session.prepare_form_preview()

        if screenshot_path and os.path.exists(screenshot_path):
            # Send screenshot
            with open(screenshot_path, 'rb') as photo:
                sent_msg = await query.message.answer_photo(
                    photo=types.FSInputFile(screenshot_path),
                    caption=f"Form preview for {job['title']}\n\n" + await apply_session.get_summary(),
                    reply_markup=apply_confirmation_keyboard()
                )

            # Store session for confirmation
            active_sessions[sent_msg.message_id] = {
                'apply_session': apply_session,
                'job': job,
                'user_id': query.from_user.id
            }

            await query.message.delete()
        else:
            await query.message.edit_text(
                f"Form preview ready:\n\n{await apply_session.get_summary()}\n\n"
                "Ready to submit?",
                reply_markup=apply_confirmation_keyboard()
            )

    except Exception as e:
        await query.message.edit_text(f"❌ Error: {str(e)[:100]}")

@router.callback_query(F.data == "confirm_apply")
async def handle_confirm_apply(query: types.CallbackQuery):
    """Handle confirm & submit."""
    try:
        msg_id = query.message.message_id
        session_data = active_sessions.get(msg_id)

        if not session_data or 'apply_session' not in session_data:
            await query.answer("❌ Session expired", show_alert=True)
            return

        apply_session = session_data['apply_session']
        job = session_data['job']

        await query.answer("⏳ Submitting application...", show_alert=False)

        # Submit
        success = await apply_session.submit_application()

        if success:
            db = await init_db()
            # Get job from DB and mark as applied
            applied_job = await db.get_job_by_id(job.get('id', 1))
            if applied_job:
                await db.mark_applied(applied_job['id'], 'applied')

            await query.message.edit_caption(
                caption=f"✅ Application submitted for {job['title']} at {job['company']}!\n\n"
                        f"Check your email for confirmation.",
                reply_markup=None
            )
        else:
            await query.message.edit_caption(
                caption=f"⚠️ Submission may have failed. Please verify at:\n{job['url']}",
                reply_markup=None
            )

        # Cleanup
        if msg_id in active_sessions:
            del active_sessions[msg_id]

    except Exception as e:
        await query.message.edit_caption(caption=f"❌ Error: {str(e)[:100]}", reply_markup=None)

@router.callback_query(F.data == "cancel_apply")
async def handle_cancel_apply(query: types.CallbackQuery):
    """Handle cancel apply."""
    msg_id = query.message.message_id
    if msg_id in active_sessions:
        del active_sessions[msg_id]

    await query.message.delete()
    await query.answer("❌ Application cancelled", show_alert=False)

@router.callback_query(F.data == "skip")
async def handle_skip(query: types.CallbackQuery):
    """Handle skip button."""
    msg_id = query.message.message_id
    if msg_id in active_sessions:
        del active_sessions[msg_id]

    await query.answer("⏭️ Job skipped.", show_alert=False)
    await query.message.delete()

@router.callback_query(F.data == "save")
async def handle_save(query: types.CallbackQuery):
    """Handle save button."""
    await query.answer("💾 Job saved for later.", show_alert=False)
