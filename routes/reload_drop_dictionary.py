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

@router.post("/items")
async def handle(whitelistData: TriggerWhitelist):
    logging.info("Reloading drop dictionary...")
    logging.info("Whitelist Data: %s", whitelistData)
    if whitelistData.triggerDictionary or whitelistData.messageFilters:
        jsonData = whitelistData
    else:
        try:
            data = requests.get(os.environ.get("API") + "/events/whitelist")
            if data.status_code != 200:
                logging.error(f"Failed to fetch item list {data.status_code}: {data.text}")
                return {"error": "Failed to fetch item list"}
            jsonData = data.json()
        except requests.RequestException as e:
            logging.error("Error fetching item list: %s", e)
            return {"error": "Failed to fetch item list"}

    logging.info("JSON Data: %s", jsonData)

    data = WhitelistData()
    if "triggerDictionary" in jsonData:
        for key, value in jsonData["triggerDictionary"].items():
            if ":" in key:
                tupleKey = tuple(key.lower().split(":"))
            else:
                tupleKey = (key.lower(), "")
            data.triggerDictionary[tupleKey] = value

        logging.info("Trigger Dictionary:")
        for key, value in data.triggerDictionary.items():
            logging.info("Key: %s, Value: %s", key, value)

    if "messageFilters" in jsonData:
        for key, value in jsonData["messageFilters"].items():
            data.messageFilters[key] = value

        logging.info("Message Filters:")
        for key, value in data.messageFilters.items():
            logging.info("Key: %s, Value: %s", key, value)

    set_whitelist_data(data)
