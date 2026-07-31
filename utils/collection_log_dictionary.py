import logging
import requests


class CollectionLogData:
    def __init__(self):
        self.item_ids: set[int] = set()


data = CollectionLogData()


def get_collection_log_ids() -> set[int]:
    """Returns the set of OSRS item ids that are on the collection log."""
    return data.item_ids


def set_collection_log_ids(item_ids: set[int]) -> None:
    data.item_ids = item_ids


def populate_collection_log_dictionary(api_url: str) -> set[int] | None:
    """Load the collection log item-id set from the backend catalog.

    Mirrors populate_drop_dictionary: the backend owns the catalog, we cache the
    ids in-memory to filter which drops to forward as collection-log events.
    """
    logging.info("Populating collection log dictionary...")
    try:
        response = requests.get(api_url + "/collection-log/items", timeout=15)
        if response.status_code != 200:
            logging.error(f"Failed to fetch collection log items {response.status_code}: {response.text}")
            return None
        item_ids = {int(i) for i in response.json()}
        set_collection_log_ids(item_ids)
        logging.info(f"Collection log dictionary populated with {len(item_ids)} items.")
        return item_ids
    except requests.RequestException as e:
        logging.error("Error populating collection log dictionary: %s", e)
        return None
