from models.submission import Submission, KillCountExtra
from .parse_response import DiscordEmbedData
from ..trigger_dictionary import get_whitelist_data
from ..submit import write
import logging

def submit_kc(rsn, discordId, boss, killCount, submitType) -> list[tuple[str, DiscordEmbedData]]:
    whitelistData = get_whitelist_data()
    
    # Print out the contents of the drop dictionary for debugging
    logging.debug("Kill Count Dictionary:")
    for key in whitelistData.killCountTriggers:
        logging.debug(f"Key: {key}")
        
    # Check if the boss is in the kill count triggers
    if boss.lower() in whitelistData.killCountTriggers:
        return write(
            player=rsn,
            discordId=discordId,
            trigger=boss,
            source=boss,
            quantity=killCount,
            totalValue=0,  # No value for kill counts
            type=submitType
        )
    
    return []

def parse_kill_count(data: Submission) -> list[tuple[str, DiscordEmbedData]]:
    notifications: list[tuple[str, DiscordEmbedData]] = []

    # Extract necessary data from the submission
    rsn = data.playerName
    discordId = data.discordUser.id if data.discordUser else "None"
    extra: KillCountExtra = data.extra
    boss = extra.boss
    count = extra.count
    
    # Get the whitelist data to check if this boss is in the kill count triggers
    whitelist = get_whitelist_data()
    
    # Check if the kill count is for a boss we care about
    if boss.lower() in whitelist.killCountTriggers:
        logging.info(f"Found whitelisted kill count for {boss} with count {count}")
        
        # Submit the kill count to the API
        for notification_data in submit_kc(rsn, discordId, boss, count, "KILL_COUNT"):
            notifications.append(notification_data)
    else:
        logging.info(f"Kill count for {boss} not in whitelist, ignoring")

    return notifications
