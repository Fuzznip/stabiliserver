from dotenv import load_dotenv
load_dotenv()
import os
import requests
import logging

from .trigger_dictionary import get_whitelist_data
from utils.request_handlers.parse_response import DiscordEmbedData, DiscordEmbedField, DiscordEmbedAuthor

def write(player: str, discordId: str, trigger: str, source: str, quantity: str, totalValue: str, type: str) -> list[tuple[str, DiscordEmbedData]]:
    # Send to the endpoint "/events/submit"
    response = requests.post(
        os.environ.get("API") + "/events/submit",
        json={
            "rsn": player,
            "id": discordId,
            "trigger": trigger,
            "source": source,
            "quantity": quantity,
            "totalValue": totalValue,
            "type": type,
        }
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

# Return value in the form of a list of tuples of item names to their lists of output ids
def submit(rsn, discordId, source, item, itemPrice, itemQuantity, submitType) -> list[tuple[str, DiscordEmbedData]]:
    whitelistData = get_whitelist_data()
    # Print out the contents of the drop dictionary for debugging
    logging.debug("Drop Dictionary:")
    for key, value in whitelistData.triggers:
        logging.debug(f"Key: {key}, Value: {value}")
        
    # Create a query for the item and source
    query = (item.lower(), source.lower())
    
    # TODO: Check blacklists

    # Check if the query is in the drop dictionary
    if query in whitelistData.triggers:
        return write(
            player=rsn,
            discordId=discordId,
            trigger=item,
            source=source,
            quantity=itemQuantity,
            totalValue=itemPrice * itemQuantity,
            type=submitType
        )

    # Check if the query is in the drop dictionary without a specific source
    query = (item.lower(), "")
    if query in whitelistData.triggers:
        return write(
            player=rsn,
            discordId=discordId,
            trigger=item,
            source=source,
            quantity=itemQuantity,
            totalValue=itemPrice * itemQuantity,
            type=submitType
        )

    return []
