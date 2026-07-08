from disnake import Client, Intents
from datetime import datetime

from src.services.database_service import DBService
from src.services.google_sheets import GoogleSheetsService
from src.services.steam.converter import ConvertSteamUrl
from src.utils.pars_data import ParsData

from config import Config

intents = Intents.default()
intents.message_content = True

pars_data = ParsData()
convert_steam_url = ConvertSteamUrl()
google_sheets_service = GoogleSheetsService()
database_service = DBService()


def create_bot(worksheet):
    bot = Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f"Бот {bot.user} запущений успішно")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        if message.author.id not in Config.ADMIN_ID:
            return

        if message.message_snapshots:
            for snapshot in message.message_snapshots:
                if snapshot.embeds:
                    for embed in snapshot.embeds:
                        data = pars_data.parseEmbed(embed.to_dict())
                        count = await write_players_to_sheet(data, worksheet, message) 

                        await message.channel.send(f'Записано {count} профілів.')

    return bot


async def write_players_to_sheet(data: list[dict], worksheet, message) -> int:
    count = 0
    date = datetime.now()
    date_format = date.strftime("%d.%m")

    for item in data:

        steam_id, resolved_url = convert_steam_url.resolveSteamUrlToId(item["steam_url"])
        item["steam_url"] = resolved_url

        status = await database_service.get_by_id("user_data", "STEAM_ID", steam_id)

        if not status:
            await database_service.create_user(steam_id, item["name"])

            row = [date_format, item["name"], resolved_url, "", "", item["value"]]
            google_sheets_service.append_row(worksheet, row)

            count += 1
        else:
            await message.channel.send(f"Гравець {item['name']} вже доданий до таблиці.")

    return count