from aiogram_dialog import DialogManager


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    """Получение списка столов с учетом выбранной вместимости."""
    user_model = dialog_manager.dialog_data["user"]
    company_name = dialog_manager.dialog_data["company_name"]

    confirmed_text = (
        "<b>Подтверждение создания компании</b>\n\n"
        f"<b>Имя компании:</b> {company_name}\n\n"
        f"<b>Администратор компании:</b> {user_model.username}\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}
