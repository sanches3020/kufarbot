from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from loader import cursor, con, router

@router.message(Command('start'))
async def handle_start(message: Message):

    command_args = message.text.split()

    if len(command_args) > 1:
        token = command_args[1] 

        cursor.execute("SELECT id FROM stats WHERE token = ?", (token,))
        result = cursor.fetchone()

        if result:

            cursor.execute("UPDATE stats SET counter = counter + 1 WHERE token = ?", (token,))
            con.commit()
            await message.answer(f"Спасибо, что перешли по ссылке! Токен {token} учтён.")
        else:
            await message.answer("Токен недействителен или не найден.")

    kb_builder = ReplyKeyboardBuilder()
    kb_builder.add(
        KeyboardButton(text='Добавить ссылку'),
        KeyboardButton(text='Удалить ссылку')
    )

    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=kb_builder.as_markup(resize_keyboard=True)
    )
