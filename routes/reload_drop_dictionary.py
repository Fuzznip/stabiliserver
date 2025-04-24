from fastapi import APIRouter, Request
from utils.trigger_dictionary import set_whitelist_data, WhitelistData
from dotenv import load_dotenv
load_dotenv()
import os
import requests
from pydantic import BaseModel
import logging

class TriggerWhitelist(BaseModel):
    triggerDictionary: dict[str, list] | None = None
    messageFilters: dict[str, list] | None = None

router = APIRouter()

async def populate_drop_dictionary(api_url: str):
    logging.info("Populating drop dictionary...")
    try:
        data = requests.get(api_url + "/events/whitelist")
        if data.status_code != 200:
            logging.error(f"Failed to fetch item list {data.status_code}: {data.text}")
            return None
        jsonData = data.json()
        logging.info("JSON Data: %s", jsonData)

        whitelist_data = WhitelistData()
        if "triggerDictionary" in jsonData:
            for key, value in jsonData["triggerDictionary"].items():
                if ":" in key:
                    tupleKey = tuple(key.lower().split(":"))
                else:
                    tupleKey = (key.lower(), "")
                whitelist_data.triggerDictionary[tupleKey] = value

        if "messageFilters" in jsonData:
            for key, value in jsonData["messageFilters"].items():
                whitelist_data.messageFilters[key] = value

        set_whitelist_data(whitelist_data)
        logging.info("Drop dictionary populated successfully.")
        return whitelist_data
    except requests.RequestException as e:
        logging.error("Error populating drop dictionary: %s", e)
        return None

@router.post("/items")
async def handle(whitelistData: TriggerWhitelist):
    logging.info("Reloading drop dictionary...")
    logging.info("Whitelist Data: %s", whitelistData)
    if whitelistData.triggerDictionary or whitelistData.messageFilters:
        jsonData = whitelistData.model_dump()
    else:
        jsonData = await populate_drop_dictionary(os.environ.get("API"))
        if not jsonData:
            return {"error": "Failed to fetch item list"}

    set_whitelist_data(jsonData)
    logging.info("Drop dictionary reloaded successfully.")
    return {"message": "Drop dictionary reloaded successfully"}
