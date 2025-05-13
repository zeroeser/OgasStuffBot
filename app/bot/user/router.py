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
async def smd_start(message: Message, state: FSMContext):
    await state.clear()

    user_data = message.from_user
    text = f"Привет {user_data.username}. Данный бот рассчитан на запрос и подтверждение закупок у компаний Мики и Кедра.\n\n Для регистрации в боте пропиши команду '/registration'"
    await message.answer(
        text,
    )


@router.message(Command("registration"))
async def registration(
    message: Message, state: FSMContext, session_with_commit: AsyncSession
):
    await state.clear()

    user_data = message.from_user
    user_id = user_data.id

    user_info = await UserDAO(session_with_commit).find_one_or_none_by_id(user_id)
    if user_info is None:
        user_schema = User(id=user_id, username=user_data.username)
        await UserDAO(session_with_commit).add(user_schema)
        text = f"Пользователь {user_data.username} успешно зарегистрированы"
        await message.answer(
            text,
        )
    else:
        await message.answer(
            "Вы уже зарегистрированы",
        )


@router.message(Command("info"))
async def info(message: Message, state: FSMContext, is_admin: bool):
    await state.clear()

    await message.answer(
        "Информация",
        reply_markup=main_user_kb(is_admin),
    )


@router.callback_query(F.data == "orders")
async def orders(
    call: CallbackQuery, session_without_commit: AsyncSession, is_admin: bool
):
    user_orders = await OrderDAO(session_without_commit).find_one_or_none_by_user_id(
        call.from_user.id
    )
    if user_orders:
        text = "У вас есть заказы"
    else:
        text = "У вас нет заказов"
    # TODO Подумать над middleware для callback, так как сейчас 'AdminMiddleware' смотрит только message
    await call.message.edit_text(text, reply_markup=main_user_kb(is_admin))
