import re

import pandas as pd

from config import get_telethon_session, setting


class Actions:

    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"[*_`~]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip().lower()

    @staticmethod
    def clean_text(text: str) -> str:
        """Удаляет лишние пробелы, переносы строк и переводит в нижний регистр."""
        if not text:
            return ""
        return " ".join(text.split()).lower()

    async def collect_all_messages(
        self, group_id=setting.DISCUSSION_CHAT_ID
    ) -> list:
        """Собираем все сообщения в Excel"""
        comments = []
        client = await get_telethon_session()
        async with client:
            async for msg in client.iter_messages(group_id, reverse=True):
                sender = await msg.get_sender()
                name = getattr(sender, "first_name", "") or ""
                username = (
                    ("@" + sender.username)
                    if getattr(sender, "username", None)
                    else ""
                )
                text = msg.text or ""
                date = (
                    msg.date.isoformat() if getattr(msg, "date", None) else ""
                )
                reply_to_id = (
                    getattr(msg.reply_to, "reply_to_msg_id", None)
                    if getattr(msg, "reply_to", None)
                    else None
                )
                comments.append(
                    [msg.id, date, reply_to_id, name, username, text]
                )
        return comments

    def all_messages_in_file(self, array, output_file=setting.OUTPUT_FILE_ALL):
        df = pd.DataFrame(
            array,
            columns=[
                "msg_id",
                "date",
                "reply_to_msg_id",
                "Имя",
                "Ник",
                "Сообщение",
            ],
        )
        df.to_excel(output_file, index=False)
        return output_file

    async def get_target_id(
        self, post_text: str, group_id=setting.DISCUSSION_CHAT_ID
    ):
        """Находит msg_id поста по тексту."""
        search_text = self.normalize_text(post_text)
        client = await get_telethon_session()
        async with client:
            async for msg in client.iter_messages(group_id, reverse=True):
                msg_content = self.normalize_text(msg.text or "")
                if search_text and search_text in msg_content:
                    return msg.id
        return None

    async def collect_replies_for_post(
        self, target_id: int, group_id=setting.DISCUSSION_CHAT_ID
    ):
        """Собирает прямые ответы к посту."""
        comments = []
        client = await get_telethon_session()
        async with client:
            async for msg in client.iter_messages(group_id, reverse=True):
                if getattr(msg.reply_to, "reply_to_msg_id", None) == target_id:
                    sender = await msg.get_sender()
                    name = getattr(sender, "first_name", "") or ""
                    username = (
                        ("@" + sender.username)
                        if getattr(sender, "username", None)
                        else ""
                    )
                    text = msg.text or ""
                    date = (
                        msg.date.isoformat()
                        if getattr(msg, "date", None)
                        else ""
                    )
                    comments.append([date, target_id, name, username, text])
        return comments

    def all_messages_post_in_file(self, array, output_file=None):
        if output_file is None:
            output_file = setting.all_comments_for_date
        df = pd.DataFrame(
            array,
            columns=["date", "reply_to_msg_id", "Имя", "Ник", "Сообщение"],
        )
        df.insert(0, "msg_id", range(1, len(df) + 1))
        df.to_excel(output_file, index=False)
        return output_file
