from models.submission import Submission
from ..submit import submit
from .parse_response import DiscordEmbedData

def parse_loot(data: Submission) -> list[tuple[str, DiscordEmbedData]]:
    screenshotItems: list[tuple[str, DiscordEmbedData]] = []

    rsn = data.playerName
    discordId = data.discordUser.id if data.discordUser else "None"
    source = data.extra.source
    items = data.extra.items

    for item in items:
        itemName = item.name
        itemPrice = item.priceEach
        itemQuantity = item.quantity

        # Check if the item is in the drop dictionary
        threadIds, embedData = submit(rsn, discordId, source, itemName, itemPrice, itemQuantity, "LOOT")
        for threadId in threadIds:
            screenshotItems.append((threadId, embedData))  # Ensure each tuple has exactly two values

    return screenshotItems
