# dropDictionary is a dictionary of pairs of items and drop sources to the list of channels they should post in
# eg. { ("abyssal whip", "abyssal demon"): [ "1233130963870154864", "1232048319996625029", ... ] }
class WhitelistData:
    triggerDictionary: dict[tuple[str, str], list[str]] = {}
    messageFilters: dict[str, list[str]] = {}

data = WhitelistData()

def get_whitelist_data() -> WhitelistData:
    """
    Returns the whitelist data.
    """
    return data

def set_whitelist_data(newWhitelistData: WhitelistData) -> None:
    """
    Sets the whitelist data.
    This is used to update the whitelist data when it is reloaded.
    """
    global data
    data = newWhitelistData
