from aiogram.fsm.state import StatesGroup, State


class OrdersState(StatesGroup):
    list = State()
    details = State()
    edit = State()
