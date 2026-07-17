import requests
import re

class ConvertSteamUrl:
    def get_steam_id(self, url: str) -> str:
        """Отримання steam_id"""
        try:
            if url.split("/")[3] == "profiles":
                return url.split("/")[4]
            elif url.split("/")[3] == "id":
                username = url.split("/")[4]
                profile_req = requests.get(f"https://steamid.io/lookup/{username}")
                match = re.search(r'\b(\d{17})\b', profile_req.text)

                if match:
                    return match.group(1)
            else:
                print(f"Неправильний тип посилання: {url}")

        except Exception as e:
            print(f" ERROR  -- -- Помилка під час коніертації url: {e}")

    def link_merging(self, steam_id: str) -> str:
        """Склеювання посилання та steam_id"""
        return ("https://steamcommunity.com/profiles/" + steam_id)
    
    def resolveSteamUrlToId(self, url: str) -> tuple[str, str]:
        """Конвертація url із username в url із steam_id
            Args:
                url: str -- Посилання на профіль гравця
            Returns:
                tuple[str, str]:
                    steam_id: str -- id гравця
                    url: str -- Посилання на профіль гравця в форматі із ID
                """
        steam_id = self.get_steam_id(url)
        url = self.link_merging(steam_id)
        return steam_id, url