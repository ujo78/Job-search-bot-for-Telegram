from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

from config import RESUME_DIR, SCREENSHOTS_DIR
from bot.keyboards import main_menu, job_digest_keyboard, apply_confirmation_keyboard
from matcher.resume_parser import parse_resume
from matcher.embedder import JobEmbedder
from storage.db import JobDB

router = Router()

class ResumeUpload(StatesGroup):
    waiting_for_resume = State()

class ApplyFlow(StatesGroup):
    confirming_apply = State()

async def init_db():
    """Initialize database."""
    db = JobDB("job_search.db")
    await db.init()
    return db

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
    """Search for jobs (placeholder)."""
    await message.answer("🔍 Searching for jobs matching your resume...")
    # This will be triggered by scheduler

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
    """Handle apply button."""
    await query.answer("📝 Preparing application form preview...", show_alert=False)
    # Form filling logic will go here

@router.callback_query(F.data == "skip")
async def handle_skip(query: types.CallbackQuery):
    """Handle skip button."""
    await query.answer("⏭️ Job skipped.", show_alert=False)

@router.callback_query(F.data == "save")
async def handle_save(query: types.CallbackQuery):
    """Handle save button."""
    await query.answer("💾 Job saved for later.", show_alert=False)
