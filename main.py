import asyncio

from config import Config
from src.services.google_sheets import GoogleSheetsService
from src.handlers.discord_handler import create_bot
from src.services.database_service import DBCreator


async def main():
    sheets_service = GoogleSheetsService()
    client = sheets_service.client_init_json()
    worksheet = sheets_service.get_table_by_url(client, Config.SHEETS_URL)

    if await DBCreator.create_tables():
        print("Таблиці бази даних успішно створені")
    else:
        print("Помилка при створенні БД")

    # Викликати лише ОДИН РАЗ (закоментувати після першого запуску)
    # sheets_service.setup_status_dropdown(worksheet, column=5)

    bot = create_bot(worksheet)
    await bot.start(Config.BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())