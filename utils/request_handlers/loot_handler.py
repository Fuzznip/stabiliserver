from models.submission import Submission
from .parse_response import DiscordEmbedData
import logging
from ..trigger_dictionary import get_whitelist_data
from ..submit import write

# Return value in the form of a list of tuples of item names to their lists of output ids
def submit_loot(rsn, discordId, source, item, itemPrice, itemQuantity, submitType) -> list[tuple[str, DiscordEmbedData]]:
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

def parse_loot(data: Submission) -> list[tuple[str, DiscordEmbedData]]:
    notifications: list[tuple[str, DiscordEmbedData]] = []

    rsn = data.playerName
    discordId = data.discordUser.id if data.discordUser else "None"
    source = data.extra.source
    items = data.extra.items

    for item in items:
        itemName = item.name
        itemPrice = item.priceEach
        itemQuantity = item.quantity

        # Check if the item is in the drop dictionary
        for notificationData in submit_loot(rsn, discordId, source, itemName, itemPrice, itemQuantity, "LOOT"):
            notifications.append(notificationData)

    return notifications
