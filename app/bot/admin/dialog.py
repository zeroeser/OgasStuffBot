from aiogram_dialog import Dialog

from .windows import get_company_name, get_company_admin, get_confirmed_windows

booking_dialog = Dialog(
    get_company_name(), get_company_admin(), get_confirmed_windows()
)
