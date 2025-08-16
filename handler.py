from aiogram import Router, types

from actions import Actions

action = Actions()

handler = Router()


@handler.message()
async def handle_forward(message: types.Message):
    post_text = message.caption
    if not post_text:
        await message.answer(
            "Пожалуйста, перешли сообщение с текстом или подписью."
        )
        return
    await message.answer("Ищу пост в группе обсуждений...")
    search_text = action.normalize_text(post_text)
    target_id = await action.get_target_id(search_text)
    await message.answer(
        f"Нашёл пост (msg_id={target_id}). Собираю комментарии..."
    )
    comments = await action.collect_replies_for_post(target_id)
    file = action.all_messages_post_in_file(comments)
    await message.answer_document(
        types.FSInputFile(file),
        caption=f"Комментарии к посту msg_id={target_id}",
    )
