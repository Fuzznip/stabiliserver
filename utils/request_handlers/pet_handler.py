from models.submission import Submission
from ..submit import write
from .parse_response import DiscordEmbedData

def submit_pet(rsn: str, discordId: str, pet_name: str) -> list[tuple[str, DiscordEmbedData]]:
    """
    Submit a pet to the API directly using the write function.
    All pets are considered valuable, so we process all of them without a whitelist.
    
    Args:
        rsn: The RuneScape name of the player
        discordId: Discord ID of the player
        pet_name: The name of the pet obtained
        
    Returns:
        A list of tuples containing thread IDs and embed data for notifications
    """
    # For pets, we use source as "PET", quantity is 1, total value is 0, and type is "PET"
    return write(
        player=rsn,
        discordId=discordId,
        trigger=pet_name,
        source="PET",
        quantity=1,
        totalValue=0,
        type="PET"
    )

def parse_pet(data: Submission) -> list[tuple[str, DiscordEmbedData]]:
    notifications: list[tuple[str, DiscordEmbedData]] = []

    # Extract necessary data from the submission
    rsn = data.playerName
    discordId = data.discordUser.id if data.discordUser else "None"
    pet_name = data.extra.petName
    
    # For pets, we process all of them without checking a whitelist
    # since pets are rare and valuable
    print(f"Processing pet: {pet_name} for player {rsn}")
    
    # Call our dedicated submit_pet function
    for notification_data in submit_pet(rsn, discordId, pet_name):
        notifications.append(notification_data)
        
    return notifications
