import os
from datetime import date

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv(".env")


class Settings:
    """Настройки приложения."""

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    DISCUSSION_CHAT_ID = os.getenv("DISCUSSION_CHAT_ID")
    OUTPUT_FILE_ALL = "Все сообщения с группы.xlsx"

    @property
    def all_comments_for_date(self):
        to_day = date.today().strftime("%Y-%m-%d")
        output_file_post = f"Розыгрыш {to_day}.xlsx"
        return output_file_post


setting = Settings()

telethon_client = TelegramClient(
    session="session", api_id=setting.API_ID, api_hash=setting.API_HASH
)


async def get_telethon_session() -> TelegramClient:
    """Подключение к клиенту тг."""
    if not telethon_client.is_connected():
        await telethon_client.connect()
    if not await telethon_client.is_user_authorized():
        await telethon_client.start()
    return telethon_client
