from aiogram import types

def main_menu():
    """Main menu keyboard."""
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="/search")],
            [types.KeyboardButton(text="/resume")],
            [types.KeyboardButton(text="/status")],
            [types.KeyboardButton(text="/history")],
        ],
        resize_keyboard=True
    )

def job_digest_keyboard():
    """Inline keyboard for job digest actions."""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="✅ Apply", callback_data="apply"),
                types.InlineKeyboardButton(text="⏭️ Skip", callback_data="skip"),
                types.InlineKeyboardButton(text="💾 Save", callback_data="save"),
            ]
        ]
    )

def apply_confirmation_keyboard():
    """Inline keyboard for apply confirmation."""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="✅ Confirm & Submit", callback_data="confirm_apply"),
                types.InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_apply"),
            ]
        ]
    )

def pagination_keyboard(page: int, total_pages: int):
    """Pagination keyboard for job digest."""
    buttons = []

    if page > 1:
        buttons.append(types.InlineKeyboardButton(text="⬅️ Prev", callback_data=f"page_{page-1}"))

    buttons.append(types.InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="page_info"))

    if page < total_pages:
        buttons.append(types.InlineKeyboardButton(text="Next ➡️", callback_data=f"page_{page+1}"))

    return types.InlineKeyboardMarkup(inline_keyboard=[buttons])
