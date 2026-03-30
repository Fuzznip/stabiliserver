class WhitelistData:
    def __init__(self):
        self.triggers: list[tuple[str, str]] = []
        self.killCountTriggers: list[str] = []
        self.messageFilters: list[tuple[str, str]] = []

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
    data.triggers = newWhitelistData.triggers
    data.killCountTriggers = newWhitelistData.killCountTriggers
    data.messageFilters = newWhitelistData.messageFilters
