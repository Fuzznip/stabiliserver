import json
import logging
import os
import requests
from pydantic import TypeAdapter
from models.submission import Submission
from models.notification_models import *
from utils.request_handlers.parse_response import DiscordEmbedData
from utils.request_handlers.death_handler import parse_death
from utils.request_handlers.collection_handler import parse_collection
from utils.request_handlers.level_handler import parse_level
from utils.request_handlers.loot_handler import parse_loot
from utils.request_handlers.slayer_handler import parse_slayer
from utils.request_handlers.quest_handler import parse_quest
from utils.request_handlers.clue_handler import parse_clue
from utils.request_handlers.kill_count_handler import parse_kill_count
from utils.request_handlers.combat_achievement_handler import parse_combat_achievement
from utils.request_handlers.pet_handler import parse_pet
from utils.request_handlers.speedrun_handler import parse_speedrun
from utils.request_handlers.barbarian_assault_gamble_handler import parse_barbarian_assault_gamble
from utils.request_handlers.player_kill_handler import parse_player_kill
from utils.request_handlers.group_storage_handler import parse_group_storage
from utils.request_handlers.grand_exchange_handler import parse_grand_exchange
from utils.request_handlers.trade_handler import parse_trade
from utils.request_handlers.leagues_area_handler import parse_leagues_area
from utils.request_handlers.leagues_relic_handler import parse_leagues_relic
from utils.request_handlers.leagues_task_handler import parse_leagues_task
from utils.request_handlers.chat_handler import parse_chat
from utils.request_handlers.login_handler import parse_login

def parse_json_data(json_data: str, file: bytes = None) -> list[tuple[str, DiscordEmbedData]]:
    data = json.loads(json_data)

    type = data.get("type")
    logging.info(f"Received event: type={type} player={data.get('playerName')!r}")

    base_data = {k: v for k, v in data.items() if k != 'extra'}
    raw_extra = data.get("extra", {})

    if type == 'DEATH':
        extra = TypeAdapter(DeathExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_death(submission)
    elif type == 'COLLECTION':
        extra = TypeAdapter(CollectionExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_collection(submission)
    elif type == 'LEVEL':
        extra = TypeAdapter(LevelExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_level(submission)
    elif type == 'LOOT':
        extra = TypeAdapter(LootExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_loot(submission, file)
    elif type == 'SLAYER':
        extra = TypeAdapter(SlayerExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_slayer(submission)
    elif type == 'QUEST':
        extra = TypeAdapter(QuestExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_quest(submission)
    elif type == 'CLUE':
        extra = TypeAdapter(ClueExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_clue(submission)
    elif type == 'KILL_COUNT':
        extra = TypeAdapter(KillCountExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_kill_count(submission)
    elif type == 'COMBAT_ACHIEVEMENT':
        extra = TypeAdapter(CombatAchievementExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_combat_achievement(submission)
    elif type == 'PET':
        extra = TypeAdapter(PetExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_pet(submission, file)
    elif type == 'SPEEDRUN':
        extra = TypeAdapter(SpeedrunExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_speedrun(submission)
    elif type == 'BARBARIAN_ASSAULT_GAMBLE':
        extra = TypeAdapter(BAGambleExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_barbarian_assault_gamble(submission)
    elif type == 'PLAYER_KILL':
        extra = TypeAdapter(PlayerKillExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_player_kill(submission)
    elif type == 'GROUP_STORAGE':
        extra = TypeAdapter(GroupStorageExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_group_storage(submission)
    elif type == 'GRAND_EXCHANGE':
        extra = TypeAdapter(GrandExchangeExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_grand_exchange(submission)
    elif type == 'TRADE':
        extra = TypeAdapter(PlayerTradeExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_trade(submission)
    elif type == 'LEAGUES_AREA':
        extra = TypeAdapter(LeaguesAreaExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_leagues_area(submission)
    elif type == 'LEAGUES_RELIC':
        extra = TypeAdapter(LeaguesRelicExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_leagues_relic(submission)
    elif type == 'LEAGUES_TASK':
        extra = TypeAdapter(LeaguesTaskExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_leagues_task(submission)
    elif type == 'CHAT':
        extra = TypeAdapter(ChatExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_chat(submission)
    elif type == 'LOGIN':
        extra = TypeAdapter(ExternalPluginExtra).validate_python(raw_extra)
        submission = Submission(**base_data, extra=extra)
        return parse_login(submission)
    else:
        print(f"Unknown type: {type}")

    return None

async def parse_dink_request(payload_json: str, file: bytes) -> None:
    logging.debug(f"{payload_json}")
    if payload_json:
        try:
            notifications: list[tuple[str, DiscordEmbedData]] = parse_json_data(payload_json, file)
            logging.debug(notifications)
            if notifications:
                for thread_id, notification in notifications:  # Ensure result is a list of tuples
                    webhook_url = os.getenv("WEBHOOK_URL")
                    if not webhook_url:
                        logging.error("WEBHOOK_URL environment variable is not set.")
                        return
                    
                    # Append thread ID as a query parameter
                    url_with_thread = f"{webhook_url}?thread_id={thread_id}"
                    
                    # Construct the embed payload
                    embed = {
                        "title": notification.title,
                        "color": notification.color,
                    }
                    
                    # Add optional fields if they exist
                    if notification.description:
                        embed["description"] = notification.description
                    if notification.thumbnailImage:
                        embed["thumbnail"] = {"url": notification.thumbnailImage}
                    if notification.author:
                        embed["author"] = {
                            "name": notification.author.name,
                            "icon_url": notification.author.icon_url,
                            "url": notification.author.url,
                        }
                    if notification.fields:
                        embed["fields"] = [
                            {
                                "name": field.name,
                                "value": field.value,
                                "inline": field.inline,
                            }
                            for field in notification.fields
                        ]
                    
                    # If an image is provided, include it in the embed
                    if file:
                        embed["image"] = {"url": "attachment://image.png"}
                    
                    payload = {
                        "embeds": [embed]  # Ensure embeds is a list of dictionaries
                    }
                    
                    # Prepare files for the request
                    files = {
                        "payload_json": (None, json.dumps(payload), "application/json"),
                        "file": ("image.png", file, "image/png")
                    } if file else {
                        "payload_json": (None, json.dumps(payload), "application/json")
                    }
                    
                    # Send the POST request
                    response = requests.post(
                        url_with_thread,
                        files=files  # Use `files` for both payload and file
                    )
                    
                    if response.status_code != 200:
                        logging.error(f"Failed to send webhook to thread {thread_id}: {response.status_code} {response.text}")
        except Exception as e:
            logging.error(f"Error parsing request: {e}")
            logging.error(json.dumps(payload_json, indent=2))
