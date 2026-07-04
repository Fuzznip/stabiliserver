from models.submission import Submission
from .parse_response import DiscordEmbedData
from ..submit import write


def parse_barbarian_assault_gamble(data: Submission) -> list[tuple[str, DiscordEmbedData]]:
    return write(
        player=data.playerName,
        discordId=data.discordUser.id if data.discordUser else "None",
        trigger="BA High Gamble",
        source="Barbarian Assault",
        quantity=1,
        totalValue=sum(item.priceEach * item.quantity for item in data.extra.items),
        type="DROP",
        img_path=None,
    )
