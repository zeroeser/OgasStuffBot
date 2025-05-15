import time
from asyncio import sleep
from uuid import UUID

from aiogram_dialog.dialog import DialogManager
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.kbd import Button
from pydantic import create_model

from app.bot.admin.kbs import admin_user_kb
from app.dao.company import CompanyDAO
from app.dao.company_admins import CompanyAdminDAO
from app.dao.user import UserDAO


async def error(message: Message, widget, manager: DialogManager, error_: ValueError):
    await message.answer("Имя компании должно быть строковым!")


async def cancel_logic(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await callback.answer("Сценарий бронирования отменен!")
    await callback.message.answer(
        "Вы отменили сценарий бронирования.", reply_markup=admin_user_kb()
    )


async def validate_company_name(
    message: Message, widget, dialog_manager: DialogManager, company_name: str
):
    session = dialog_manager.middleware_data.get("session_without_commit")
    company_filter = create_model("CompanyModel", name=(str, ...))(name=company_name)

    company = await CompanyDAO(session).find_one_or_none(company_filter)
    if company:
        await message.answer("⚠️ Компания с таким именем уже существует!")
        return

    dialog_manager.dialog_data["company_name"] = company_name
    await dialog_manager.next()


async def validate_user(
    message: Message, widget, dialog_manager: DialogManager, user_id: int
):
    session = dialog_manager.middleware_data.get("session_without_commit")
    user = await UserDAO(session).find_one_or_none_by_id(user_id)
    if user is None:
        await message.answer("⚠️ Такого пользователя не существует в базе данных")
        return

    dialog_manager.dialog_data["user"] = user
    await dialog_manager.next()


async def on_confirmation(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """Обработчик подтверждения бронирования."""
    session = dialog_manager.middleware_data.get("session_with_commit")

    # Получаем выбранные данные
    user = dialog_manager.dialog_data["user"]
    company_name = dialog_manager.dialog_data["company_name"]

    add_company = create_model("CompanyModel", name=(str, ...))(name=company_name)

    await callback.message.edit_text("Приступаю к сохранению")
    await sleep(0.5)

    company = await CompanyDAO(session).add(add_company)
    company_admin_model = create_model(
        "CompanyAdminModel", user_id=(int, ...), company_id=(UUID, ...)
    )(user_id=user.id, company_id=company.id)

    await CompanyAdminDAO(session).add(company_admin_model)
    await callback.message.edit_text("Компания успешно создана")

    await dialog_manager.done()
