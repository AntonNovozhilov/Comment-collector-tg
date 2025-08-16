from aiogram import Router, types
from aiogram.filters import Command

from actions import Actions

action = Actions()

command = Router()


@command.message(Command("collect_all"))
async def cmd_collect_all(message: types.Message):
    await message.answer("Начинаю сбор всех сообщений из группы обсуждений...")
    try:
        all_comments = await action.collect_all_messages()
        file_all = action.all_messages_in_file(all_comments)
        await message.answer_document(
            types.FSInputFile(file_all), caption="Все сообщения (Excel)"
        )
    except Exception as e:
        await message.answer(f"Ошибка при сборе всех сообщений: {e}")
