import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("TOKEN")

    # Bots or admins ID the bot will listen to
    ADMIN_ID = [int(x) for x in os.getenv("ADMIN_ID").split(",")]

    JSON_CONFIG_PATH = os.getenv("JSON_CONFIG_PATH")

    SHEETS_ID = os.getenv("SHEETS_ID")
    SHEETS_URL = os.getenv("SHEETS_URL")

    @classmethod
    def validate(cls):
        """Checking that all necessary settings are present"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не налаштовано")
        if not cls.ADMIN_ID:
            raise ValueError("ADMIN_ID не налаштовано")

# Checking the configuration during import
Config.validate()