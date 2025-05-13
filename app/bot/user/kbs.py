from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_user_kb(is_admin: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="Заказы", callback_data="orders"))

    if is_admin:
        kb.add(InlineKeyboardButton(text="Админ-панель", callback_data="admin_panel"))

    kb.adjust(1)
    return kb.as_markup()
