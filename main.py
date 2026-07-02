from config import Config
from src.services.google_sheets import GoogleSheetsService
from src.handlers.discord_handler import create_bot


def main():
    sheets_service = GoogleSheetsService()
    client = sheets_service.client_init_json()
    worksheet = sheets_service.get_table_by_url(client, Config.SHEETS_URL)

    # Викликати лише ОДИН РАЗ (наприклад, закоментувати після першого запуску)
    sheets_service.setup_status_dropdown(worksheet, column=5)

    bot = create_bot(worksheet)
    bot.run(Config.BOT_TOKEN)


if __name__ == "__main__":
    main()