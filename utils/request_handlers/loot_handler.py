from models.submission import Submission
from models.notification_models import LootExtra

def parse_loot(data: Submission) -> dict[str, list[str]]:
    screenshotItems: dict[str, list[str]] = {}

    rsn = data.playerName
    if data.discordUser is None:
        discordId = "None"
    else:
        discordId = data.discordUser.id

    source = data.extra.source
    items = data.extra.items

    for item in items:
        itemName = item.name
        itemPrice = item.priceEach
        itemQuantity = item.quantity
        itemTotal = itemPrice * itemQuantity

        # Check if the item is in the drop dictionary
        output = submit(rsn, discordId, source, itemName, itemPrice, itemQuantity, "LOOT")
        if output is not None:
            threadIds = output["threadList"]
            for threadId in threadIds:
                if threadId not in screenshotItems:
                    screenshotItems[threadId] = []

                if "message" in output:
                    screenshotItems[threadId].append(output["message"])
                else:
                    screenshotItems[threadId].append(itemName)

    return screenshotItems
