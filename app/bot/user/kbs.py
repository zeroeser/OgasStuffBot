from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import settings


def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="Заказы", callback_data="orders"))

    # TODO надо заменить проверку на что-то нормальное
    if str(user_id) in settings.ADMIN_IDS:
        kb.add(InlineKeyboardButton(text="Админ-панель", callback_data="admin_panel"))

    kb.adjust(1)
    return kb.as_markup()
