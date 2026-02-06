from models.submission import Submission
from utils.s3_upload import upload_to_s3
from .parse_response import DiscordEmbedData
from ..submit import write

def winter_bingo_2026_check_totem_quantity(trigger: str) -> int:
    # Check if "offerings five times" is in the trigger
    if "you rummage through the offerings five times" in trigger.lower():
        return 5
    elif "you rummage through the offerings" in trigger.lower():
        return 1
    return 1

def parse_chat(data: Submission, file: bytes | None = None) -> list[tuple[str, DiscordEmbedData]]:
    img_path = None
    if file:
        img_path = upload_to_s3(file)

    return write(
        player=data.playerName,
        discordId=data.discordUser.id if data.discordUser else "None",
        trigger=data.extra.message,
        source=data.extra.source,
        quantity=winter_bingo_2026_check_totem_quantity(data.extra.message),
        totalValue=0,
        type="CHAT",
        img_path=img_path
    )
