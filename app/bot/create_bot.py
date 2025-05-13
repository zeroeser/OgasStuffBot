from locale import Error, LC_TIME, setlocale

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram_dialog import setup_dialogs
from loguru import logger

from app.core.config import settings
from app.bot.admin.router import router as admin_router
from app.bot.user.router import router as user_router
from app.core.middlewares import (
    AdminMiddleware,
    DatabaseMiddlewareWithCommit,
    DatabaseMiddlewareWithoutCommit,
)

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())  # TODO: Заменить на что-нибудь нормальное


async def set_commands():
    commands = [BotCommand(command="start", description="Старт")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


def set_russian_locale():
    try:
        # Пробуем установить локаль для Windows
        setlocale(LC_TIME, "Russian_Russia.1251")
    except Error:
        try:
            # Пробуем установить локаль для Linux/macOS
            setlocale(LC_TIME, "ru_RU.utf8")
        except Error:
            # Игнорируем ошибку, если локаль не поддерживается
            pass


async def init_bot():
    set_russian_locale()
    setup_dialogs(dp)
    await set_commands()

    dp.message.middleware(DatabaseMiddlewareWithoutCommit())
    dp.message.middleware(DatabaseMiddlewareWithCommit())
    dp.message.middleware(AdminMiddleware())

    dp.include_router(user_router)
    dp.include_router(admin_router)

    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(admin_id, f"Бот запущен🥳.")
        except:
            pass
    logger.info("Бот успешно запущен.")


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(admin_id, "Бот остановлен.")
    except:
        pass
    logger.error("Бот остановлен!")
