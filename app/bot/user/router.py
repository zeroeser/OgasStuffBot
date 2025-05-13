from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from app.bot.user.kbs import main_user_kb

router = Router()


@router.message(CommandStart())
async def smd_start(message: Message, state: FSMContext, is_admin: bool):
    await state.clear()

    user_data = message.from_user
    user_id = user_data.id
    text = "Привет админ" if is_admin else "Привет пользователь"
    await message.answer(
        text,
        reply_markup=main_user_kb(is_admin),
    )
