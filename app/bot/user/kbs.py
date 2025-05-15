from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def main_user_kb(is_admin: bool) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="Регистрация"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="Заказы"), KeyboardButton(text="Корзина")],
    ]
    if is_admin:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    kb = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:",
    )
    return kb
