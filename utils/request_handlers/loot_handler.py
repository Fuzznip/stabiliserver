from models.submission import Submission
from ..submit import submit
from .parse_response import DiscordEmbedData

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
        for notificationData in submit(rsn, discordId, source, itemName, itemPrice, itemQuantity, "LOOT"):
            notifications.append(notificationData)

    return notifications
