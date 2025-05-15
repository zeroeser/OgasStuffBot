from aiogram.fsm.state import StatesGroup, State


class CompanyCreatingState(StatesGroup):
    company_name = State()
    tg_user_id = State()
    confirmation = State()
