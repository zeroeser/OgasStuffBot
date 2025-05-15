from aiogram_dialog import (
    Window,
)
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Cancel,
)

from app.bot.admin.getters import get_confirmed_data
from app.bot.admin.handlers import (
    validate_company_name,
    error,
    validate_user,
    cancel_logic,
    on_confirmation,
)
from app.bot.admin.state import CompanyCreatingState


def get_company_name() -> Window:
    return Window(
        Const("Введите имя компании:"),
        TextInput(
            id="company_name",
            on_success=validate_company_name,
            on_error=error,
            type_factory=str,
        ),
        state=CompanyCreatingState.company_name,
    )


def get_company_admin() -> Window:
    return Window(
        Const("Введите телеграмм идентификатор пользователя:"),
        TextInput(id="company_admin", on_success=validate_user, type_factory=int),
        state=CompanyCreatingState.tg_user_id,
    )


def get_confirmed_windows():
    return Window(
        Format("{confirmed_text}"),
        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_confirmation),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),
        state=CompanyCreatingState.confirmation,
        getter=get_confirmed_data,
    )
