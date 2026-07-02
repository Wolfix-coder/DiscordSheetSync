from disnake import Client, Intents

from src.services.google_sheets import GoogleSheetsService
from src.services.steam.converter import ConvertSteamUrl
from src.utils.pars_data import ParsData

from config import Config

intents = Intents.default()
intents.message_content = True

pars_data = ParsData()
convert_steam_url = ConvertSteamUrl()
google_sheets_service = GoogleSheetsService()


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
                        write_players_to_sheet(data, worksheet)

    return bot


def write_players_to_sheet(data: list[dict], worksheet):
    for item in data:
        resolved_url = convert_steam_url.resolveSteamUrlToId(item["steam_url"])
        item["steam_url"] = resolved_url

        row = ["", item["name"], resolved_url, "", "", item["value"]]
        google_sheets_service.append_row(worksheet, row)