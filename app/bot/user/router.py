from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.message import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.user.kbs import main_user_kb
from app.bot.user.schemas import User
from app.dao.orders import OrderDAO
from app.dao.user import UserDAO

router = Router()


@router.message(CommandStart())
async def smd_start(message: Message, state: FSMContext, is_admin: bool):
    await state.clear()

    user_data = message.from_user
    text = f"Привет {user_data.username}. Данный бот рассчитан на запрос мерча у компаний Мики и Кедра."
    await message.answer(text, reply_markup=main_user_kb(is_admin))


@router.message(F.text == "Регистрация")
async def registration(message: Message, session_with_commit: AsyncSession):
    user_data = message.from_user
    user_id = user_data.id

    user_info = await UserDAO(session_with_commit).find_one_or_none_by_id(user_id)
    if user_info is None:
        user_schema = User(id=user_id, username=user_data.username)
        await UserDAO(session_with_commit).add(user_schema)
        text = f"Пользователь {user_data.username} успешно зарегистрирован"
        await message.answer(
            text,
        )
    else:
        await message.answer(
            "Вы уже зарегистрированы",
        )


@router.message(Command("info"))
async def info(message: Message):

    await message.answer(
        "Тут информация об проекте",
    )


@router.message(F.text == "Заказы")
async def orders(message: Message, session_without_commit: AsyncSession):
    user_orders = await OrderDAO(session_without_commit).find_one_or_none_by_user_id(
        message.from_user.id
    )
    if user_orders:
        text = "У вас есть заказы"
    else:
        text = "У вас нет заказов"
    await message.answer(text)
