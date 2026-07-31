from models.submission import Submission
from .parse_response import DiscordEmbedData
import logging
from ..trigger_dictionary import get_whitelist_data
from ..collection_log_dictionary import get_collection_log_ids
from ..submit import write
from ..s3_upload import upload_to_s3

# TODO: Check blacklists
def is_whitelisted(item: str, source: str) -> bool:
    """Check if an item/source combo matches the whitelist."""
    whitelistData = get_whitelist_data()
    query = (item.lower(), source.lower())
    if query in whitelistData.triggers:
        return True
    query = (item.lower(), "")
    if query in whitelistData.triggers:
        return True
    return False

def is_collection_log_item(item_id: int) -> bool:
    """Check if a dropped item is tracked on the clan collection log."""
    return item_id in get_collection_log_ids()

# Return value in the form of a list of tuples of item names to their lists of output ids
def submit_loot(rsn, discordId, source, item, itemPrice, itemQuantity, submitType, img_path: str | None = None) -> list[tuple[str, DiscordEmbedData]]:
    if is_whitelisted(item, source):
        return write(
            player=rsn,
            discordId=discordId,
            trigger=item,
            source=source,
            quantity=itemQuantity,
            totalValue=itemPrice * itemQuantity,
            type=submitType,
            img_path=img_path
        )

    logging.info(f"Item not whitelisted, skipping: rsn={rsn!r} item={item!r} source={source!r}")
    return []

def parse_loot(data: Submission, file: bytes = None) -> list[tuple[str, DiscordEmbedData]]:
    notifications: list[tuple[str, DiscordEmbedData]] = []

    rsn = data.playerName
    discordId = data.discordUser.id if data.discordUser else "None"
    source = data.extra.source
    items = data.extra.items

    # Upload to S3 once if file provided and any item is a whitelisted drop or a
    # collection log item (both attach the screenshot).
    img_path = None
    if file:
        has_relevant_item = any(
            is_whitelisted(item.name, source) or is_collection_log_item(item.id)
            for item in items
        )
        if has_relevant_item:
            img_path = upload_to_s3(file)

    for item in items:
        itemName = item.name
        itemPrice = item.priceEach
        itemQuantity = item.quantity

        # Event drops (whitelist-gated).
        for notificationData in submit_loot(rsn, discordId, source, itemName, itemPrice, itemQuantity, "LOOT", img_path):
            notifications.append(notificationData)

        # Clan collection log: forward every received clog item (independent of
        # the event whitelist) so the site tracks any clog drop from any member.
        if is_collection_log_item(item.id):
            write(
                player=rsn,
                discordId=discordId,
                trigger=itemName,
                source=source,
                quantity=itemQuantity,
                totalValue=itemPrice * itemQuantity,
                type="CLOG",
                img_path=img_path,
                item_id=item.id,
            )

    return notifications
