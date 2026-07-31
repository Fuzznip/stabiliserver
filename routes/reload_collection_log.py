from fastapi import APIRouter
from dotenv import load_dotenv
load_dotenv()
import os
import logging

from utils.collection_log_dictionary import populate_collection_log_dictionary

router = APIRouter()


@router.post("/collection-log/reload")
async def handle():
    """Reload the cached collection log item-id set from the backend catalog."""
    logging.info("Reloading collection log dictionary...")
    item_ids = populate_collection_log_dictionary(os.environ.get("API"))
    if item_ids is None:
        return {"error": "Failed to fetch collection log items"}
    return {"message": f"Collection log dictionary reloaded with {len(item_ids)} items"}
