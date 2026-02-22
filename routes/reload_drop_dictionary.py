from fastapi import APIRouter, Request
from utils.trigger_dictionary import set_whitelist_data, WhitelistData
from dotenv import load_dotenv
load_dotenv()
import os
import requests
from pydantic import BaseModel
import logging

class TriggerWhitelist(BaseModel):
    dropTriggers: set[str] | None = None
    killCountTriggers: set[str] | None = None
    messageFilters: set[str] | None = None

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

        whitelistData = WhitelistData()
        if "triggers" in jsonData:
            for value in jsonData["triggers"]:
                if ":" in value:
                    whitelistData.triggers.append(tuple(value.lower().split(":", 1)))
                else:
                    whitelistData.triggers.append((value.lower(), ""))

        if "killCountTriggers" in jsonData:
            whitelistData.killCountTriggers = jsonData["killCountTriggers"]

        if "messageFilters" in jsonData:
            for value in jsonData["messageFilters"]:
                if ":" in value:
                    whitelistData.messageFilters.append(tuple(value.lower().split(":", 1)))
                else:
                    whitelistData.messageFilters.append((value.lower(), ""))

        set_whitelist_data(whitelistData)
        logging.info("Drop dictionary populated successfully.")
        return whitelistData
    except requests.RequestException as e:
        logging.error("Error populating drop dictionary: %s", e)
        return None

@router.post("/items")
async def handle(whitelistData: TriggerWhitelist):
    logging.info("Reloading drop dictionary...")
    logging.info("Whitelist Data: %s", whitelistData)
    if whitelistData.dropTriggers or whitelistData.messageFilters or whitelistData.killCountTriggers:
        jsonData = whitelistData.model_dump()
    else:
        jsonData = await populate_drop_dictionary(os.environ.get("API"))
        if not jsonData:
            return {"error": "Failed to fetch item list"}

    set_whitelist_data(jsonData)
    logging.info("Drop dictionary reloaded successfully.")
    return {"message": "Drop dictionary reloaded successfully"}
