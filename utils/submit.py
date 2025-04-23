from dotenv import load_dotenv
load_dotenv()

from drop_dictionary import get_drop_dictionary

trackedItems = []

def write(player: str, discordId: str, itemSource: str, itemName: str, itemValue: int, itemQuantity: int, submitType: str) -> None:
    pass

# Return value in the form of a list of tuples of item names to their lists of output ids
def submit(rsn, discordId, source, item, itemPrice, itemQuantity, submitType):
    output = {
        "threadList": [],
        "message": None
    }
    # result = tile_race.parse_tile_race_submission(submitType, rsn, discordId, source, item, itemPrice, itemQuantity)
    # if result is not None:
    #     output["threadList"].append(result["thread_id"])
    #     output["message"] = result["message"]

    dropDictionary = get_drop_dictionary()
    # Create a query for the item and source
    query = (item.lower(), source.lower())
    
    # TODO: Check blacklists

    # Check if the query is in the drop dictionary
    if query in dropDictionary:
        for threadId in dropDictionary[query]:
            output["threadList"].append(threadId)
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")
        return output

    # Check if the query is in the drop dictionary without a specific source
    query = (item.lower(), "")
    if query in dropDictionary:
        for threadId in dropDictionary[query]:
            output["threadList"].append(threadId)
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")
        return output
    
    # If the query is not in the drop dictionary, check if the item is in the tracked items
    if item.lower() in trackedItems:
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")

    if item.lower() + ":" + source.lower() in trackedItems:
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")

    return output
