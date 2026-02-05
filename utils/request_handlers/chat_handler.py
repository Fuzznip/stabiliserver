from models.submission import Submission
from utils.s3_upload import upload_to_s3
from .parse_response import DiscordEmbedData
from ..submit import write

def parse_chat(data: Submission, file: bytes | None = None) -> list[tuple[str, DiscordEmbedData]]:
    img_path = None
    if file:
        img_path = upload_to_s3(file)

    return write(
        player=data.playerName,
        discordId=data.discordUser.id if data.discordUser else "None",
        trigger=data.extra.message,
        source=data.extra.source,
        quantity=1,
        totalValue=0,
        type="CHAT",
        img_path=img_path
    )
