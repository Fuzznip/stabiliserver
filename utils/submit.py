from dotenv import load_dotenv
load_dotenv()
import os
import requests
import logging

from .trigger_dictionary import get_whitelist_data
from utils.request_handlers.parse_response import DiscordEmbedData, DiscordEmbedField, DiscordEmbedAuthor

def write(player: str, discordId: str, trigger: str, source: str, quantity: str, totalValue: str, type: str, img_path: str = None) -> list[tuple[str, DiscordEmbedData]]:
    # Send to the endpoint "/events/submit"
    payload = {
        "rsn": player,
        "id": discordId,
        "trigger": trigger,
        "source": source,
        "quantity": quantity,
        "totalValue": totalValue,
        "type": type,
    }
    if img_path:
        payload["img_path"] = img_path

    response = requests.post(
        os.environ.get("API") + "/events/submit",
        json=payload
    )

    if response.status_code != 200:
        logging.error(f"Failed to write data ({response.status_code} - {response.text})")
        return ([], None)
    
    jsonData = response.json()
    returnList: list[tuple[str, DiscordEmbedData]] = []
    for notification in jsonData["notifications"]:
        embedData = DiscordEmbedData(
            title=notification.get("title", "Submission"),
            color=notification.get("color", 0x992D22),  # Default color (dark red)
            thumbnailImage=notification.get("thumbnailImage", None),
            author=DiscordEmbedAuthor(
                name=notification["author"]["name"],
                icon_url=notification["author"]["icon_url"] if "icon_url" in notification["author"] else None,
                url=notification["author"]["url"] if "url" in notification["author"] else None
            ) if "author" in notification else None,
            description=notification.get("description", None),
            fields=[
                DiscordEmbedField(
                    name=field["name"],
                    value=field["value"],
                    inline=field.get("inline", False)
                ) for field in notification.get("fields", [])
            ] if "fields" in notification else None
        )
        # Append the thread ID and embed data to the return list
        returnList.append((notification["threadId"], embedData))
    
    return returnList
