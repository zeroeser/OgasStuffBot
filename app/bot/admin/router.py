from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Filter
from loguru import logger

from app.core.config import settings

router = Router()


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        logger.info(message.from_user.id in settings.ADMIN_IDS)
        return message.from_user.id in settings.ADMIN_IDS


@router.callback_query(IsAdmin(), F.text == "admin_panel")
async def admin_start(call: CallbackQuery):
    await call.answer("Доступ в админ-панель разрешен!")
    await call.message.edit_text("Тест")
