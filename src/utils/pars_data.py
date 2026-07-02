import re

class ParsData:
    def parseEmbed(self, embed: dict) -> list[dict]:
        description = embed.get("description", "")
        players = []
    
        pattern = r'\*\*\d+\.\s*\[(.*?)\]\((https://steamcommunity\.com/profiles/\d+)\)\*\*\s*—\s*\*\*\$(.*?)\*\*'
    
        for match in re.finditer(pattern, description):
            players.append({
                "name": match.group(1),
                "steam_url": match.group(2),
                "value": float(match.group(3).replace(",", "")),
            })
    
        return players