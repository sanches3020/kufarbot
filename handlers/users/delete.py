from aiogram.types import Message
from loader import router, cursor,con, scheduler
from aiogram import F


@router.message(F.text == "Удалить ссылку")
async def handle_remove_link(message: Message):
    id = message.from_user.id

    cursor.execute("SELECT id_task FROM MyTable WHERE id = ?", (id,))
    result = cursor.fetchone()

    if not result:
        await message.answer("Вы не добавляли ссылку.")
        return

    id_task = result[0]
    
    scheduler.remove_job(id_task)
    
    cursor.execute("DELETE FROM MyTable WHERE id = ?", (id,))
    con.commit()

    await message.answer("Ссылка успешно удалена.")



    