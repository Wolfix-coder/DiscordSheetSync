import requests

class ConvertSteamUrl:
    def get_steam_id(self, url: str) -> str:
        """Отримання steam_id"""
        try:
            profile_req = requests.get(url)
            steamid = str(profile_req.text.split("\"steamid\":\"")[1].split("\"")[0])
            return steamid
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