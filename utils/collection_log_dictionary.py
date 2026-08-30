import logging
import os
import requests

_DISABLED_VALUES = {"false", "0", "no", "off"}


def clan_collection_log_enabled() -> bool:
    """Whether to record clan collection log drops.

    Set CLAN_COLLECTION_LOG_ENABLED=false to stop tracking. This gates the CLOG
    submissions and the S3 screenshot uploads they would otherwise trigger, so
    turning it off drops the whole cost of the feature. Defaults to enabled, so
    an unset environment keeps the existing behaviour.
    """
    value = os.environ.get("CLAN_COLLECTION_LOG_ENABLED", "true")
    return value.strip().lower() not in _DISABLED_VALUES


class CollectionLogData:
    def __init__(self):
        self.item_ids: set[int] = set()
        # Lowercased name -> item id, for the pet path: PetExtra has no itemId.
        self.ids_by_name: dict[str, int] = {}


data = CollectionLogData()


def get_collection_log_ids() -> set[int]:
    """Returns the set of OSRS item ids that are on the collection log."""
    return data.item_ids


def get_collection_log_item_id(name: str) -> int | None:
    """Resolve a collection log item name to its id, or None if it isn't one."""
    return data.ids_by_name.get(name.strip().lower()) if name else None


def set_collection_log_ids(item_ids: set[int], ids_by_name: dict[str, int]) -> None:
    data.item_ids = item_ids
    data.ids_by_name = ids_by_name


def populate_collection_log_dictionary(api_url: str) -> set[int] | None:
    """Load the collection log item-id set from the backend catalog.

    Mirrors populate_drop_dictionary: the backend owns the catalog, we cache the
    ids in-memory to filter which drops to forward as collection-log events.
    Reads /collection-log/catalog rather than /collection-log/items because it
    carries names as well as ids, which the pet path needs.
    """
    logging.info("Populating collection log dictionary...")
    try:
        response = requests.get(api_url + "/collection-log/catalog", timeout=15)
        if response.status_code != 200:
            logging.error(f"Failed to fetch collection log items {response.status_code}: {response.text}")
            return None
        item_ids = set()
        ids_by_name = {}
        for category in response.json():
            for page in category["pages"]:
                for item in page["items"]:
                    item_ids.add(item["item_id"])
                    ids_by_name.setdefault(item["name"].strip().lower(), item["item_id"])
        set_collection_log_ids(item_ids, ids_by_name)
        logging.info(f"Collection log dictionary populated with {len(item_ids)} items.")
        return item_ids
    except requests.RequestException as e:
        logging.error("Error populating collection log dictionary: %s", e)
        return None
