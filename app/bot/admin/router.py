from loguru import logger
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, hpre
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.admin.kbs import admin_user_kb
from app.bot.admin.state import CompanyCreatingState
from app.core.config import settings
from app.dao.company import CompanyDAO

router = Router()


@router.message(F.text == "⚙️ Админ панель")
async def admin_start(message: Message, is_admin: bool):
    logger.info("Запрос команды ⚙️ Админ панель")
    if is_admin:
        await message.answer("Доступ в админ-панель разрешен!")
        await message.answer("Выберите действие:", reply_markup=admin_user_kb())


@router.callback_query(F.data == "add_company", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_add_company(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Запрос команды создания компании")

    await call.answer("Создание компании")
    await dialog_manager.start(
        state=CompanyCreatingState.company_name, mode=StartMode.RESET_STACK
    )


@router.callback_query(
    F.data == "get_companies", F.from_user.id.in_(settings.ADMIN_IDS)
)
async def admin_add_company(call: CallbackQuery, session_without_commit: AsyncSession):
    logger.info("Запрос команды вывода всех компаний")
    await call.answer("Загружаю статистику...")
    companies = await CompanyDAO(session_without_commit).find_all()
    company_list = "\n".join(
        f"🏛 {hbold(f'{idx + 1}. {company.name}')}\n"
        f"   👑 Админов: {hbold(len(company.administrators))}\n"
        f"   🆔 ID: {hpre(company.id)}\n"
        for idx, company in enumerate(companies)
    )
    await call.message.answer(
        "📋 Список всех компаний:\n\n" + company_list,
        reply_markup=admin_user_kb(),
    )


@router.callback_query(
    F.data == "delete_company", F.from_user.id.in_(settings.ADMIN_IDS)
)
async def admin_delete_company(
    call: CallbackQuery, session_without_commit: AsyncSession
):
    logger.info("Запрос удаления компании")
    companies = await CompanyDAO(session_without_commit).find_all()
    count_company = len(companies)
    if count_company:
        await call.message.answer(
            "Компания удалена",
            reply_markup=admin_user_kb(),
        )
    else:
        await call.message.answer(
            "Компаний нет",
            reply_markup=admin_user_kb(),
        )
