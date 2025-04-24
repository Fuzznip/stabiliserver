from dotenv import load_dotenv
load_dotenv()

from .trigger_dictionary import get_whitelist_data
from utils.request_handlers.parse_response import DiscordEmbedData, DiscordEmbedField, DiscordEmbedAuthor

def write(player: str, discordId: str, trigger: str, source: str, quantity: str, totalValue: str, type: str) -> None:
    data = DiscordEmbedData(
        title=f"{player}: {trigger} from {source}",
        thumbnailImage="https://i.imgur.com/4LdSYto.jpeg",
        author=DiscordEmbedAuthor(name="ToA Suckers"),
        description=f"They have been awarded 10 coins and a 4 sided die!",
        fields=[
            DiscordEmbedField(name="Stars", value="6", inline=True),
            DiscordEmbedField(name="Coins", value="144", inline=True),
            DiscordEmbedField(name="Island", value="Island of Stone", inline=True),
        ]
    )
    
    return (["1364704619498045490"], data)

# Return value in the form of a list of tuples of item names to their lists of output ids
def submit(rsn, discordId, source, item, itemPrice, itemQuantity, submitType) -> tuple[list[str], DiscordEmbedData]:
    whitelistData = get_whitelist_data()
    # Print out the contents of the drop dictionary for debugging
    print("Drop Dictionary:")
    for key, value in whitelistData.triggerDictionary.items():
        print(f"Key: {key}, Value: {value}")
        
    # Create a query for the item and source
    query = (item.lower(), source.lower())
    
    # TODO: Check blacklists

    # Check if the query is in the drop dictionary
    if query in whitelistData.triggerDictionary:
        threadList, embedData = write(
            player=rsn,
            discordId=discordId,
            trigger=item,
            source=source,
            quantity=itemQuantity,
            totalValue=itemPrice * itemQuantity,
            type=submitType
        )
        
        return (threadList, embedData)

    # Check if the query is in the drop dictionary without a specific source
    query = (item.lower(), "")
    if query in whitelistData.triggerDictionary:
        threadList, embedData = write(
            player=rsn,
            discordId=discordId,
            trigger=item,
            source=source,
            quantity=itemQuantity,
            totalValue=itemPrice * itemQuantity,
            type=submitType
        )
        
        return (threadList, embedData)

    return ([], None)
