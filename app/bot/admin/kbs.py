from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="Добавить компанию", callback_data="add_company"))
    kb.add(
        InlineKeyboardButton(
            text="Вывести список всех компаний", callback_data="get_companies"
        )
    )
    kb.add(
        InlineKeyboardButton(text="Удалить компанию", callback_data="delete_company")
    )

    kb.adjust(1)
    return kb.as_markup()
