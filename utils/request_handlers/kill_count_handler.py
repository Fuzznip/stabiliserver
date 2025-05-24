from models.submission import Submission
from ..submit import write
from .parse_response import DiscordEmbedData
from ..trigger_dictionary import get_whitelist_data

def submit_kill_count(rsn: str, discordId: str, boss: str, count: int) -> list[tuple[str, DiscordEmbedData]]:
    """
    Submit a kill count to the API directly using the write function.
    Kill counts are submitted only if they are in the whitelist.
    
    Args:
        rsn: The RuneScape name of the player
        discordId: Discord ID of the player
        boss: The name of the boss
        count: The kill count number
        
    Returns:
        A list of tuples containing thread IDs and embed data for notifications
    """
    return write(
        player=rsn,
        discordId=discordId,
        trigger=boss,
        source=boss,
        quantity=count,
        totalValue=0,
        type="KC"
    )

def parse_kill_count(data: Submission) -> list[tuple[str, DiscordEmbedData]]:
    notifications: list[tuple[str, DiscordEmbedData]] = []

    # Extract necessary data from the submission
    rsn = data.playerName
    discordId = data.discordUser.id if data.discordUser else "None"
    boss = data.extra.boss
    count = data.extra.count
    
    # Get the whitelist data to check if this boss is in the kill count triggers
    whitelist = get_whitelist_data()
    
    # Check if the kill count is for a boss we care about (case insensitive)
    if boss.lower() in [b.lower() for b in whitelist.killCountTriggers]:
        print(f"Found whitelisted kill count for {boss} with count {count}")
        
        # Submit the kill count to the API using our dedicated function
        for notification_data in submit_kill_count(rsn, discordId, boss, 1): # Since the submission cannot be more than 1 kill at a time through automatic subnmission, set count to 1 here
            notifications.append(notification_data)
    else:
        print(f"Kill count for {boss} not in whitelist, ignoring")

    return notifications
