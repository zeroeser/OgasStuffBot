import asyncio
from contextlib import asynccontextmanager
from aiogram.types import Update
from fastapi import FastAPI, Request
from loguru import logger

from app.bot.create_bot import dp, init_bot, bot, stop_bot
from app.core.config import settings


async def start_polling():
    """Function to start the bot in polling mode"""
    logger.info("Запуск бота в режиме polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка в режиме polling: {e}")
    finally:
        logger.info("Polling остановлен")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Бот запущен...")
    await init_bot()
    if settings.use_webhook:
        webhook_url = settings.hook_url
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        logger.success(f"Вебхук установлен: {webhook_url}")
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.create_task(start_polling())
    yield
    logger.info("Бот остановлен...")
    await stop_bot()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logger.info("Получен запрос с вебхука.")
    try:
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        logger.info("Обновление успешно обработано.")
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления с вебхука: {e}")
