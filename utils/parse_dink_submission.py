import json
import uuid
import logging
from pydantic import TypeAdapter
from models.submission import Submission
from models.notification_models import *
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

def parse_json_data(json_data: str) -> dict[str, list[str]]:
    data = json.loads(json_data)
    submission = Submission(**data)
    print(submission)

    type = submission.type
    if type == 'DEATH':
        return parse_death(submission)
    elif type == 'COLLECTION':
        submission.extra = TypeAdapter(CollectionExtra).validate_python(submission.extra)
        return parse_collection(submission)
    elif type == 'LEVEL':
        submission.extra = TypeAdapter(LevelExtra).validate_python(submission.extra)
        return parse_level(submission)
    elif type == 'LOOT':
        submission.extra = TypeAdapter(LootExtra).validate_python(submission.extra)
        return parse_loot(submission)
    elif type == 'SLAYER':
        submission.extra = TypeAdapter(SlayerExtra).validate_python(submission.extra)
        return parse_slayer(submission)
    elif type == 'QUEST':
        submission.extra = TypeAdapter(QuestExtra).validate_python(submission.extra)
        return parse_quest(submission)
    elif type == 'CLUE':
        submission.extra = TypeAdapter(ClueExtra).validate_python(submission.extra)
        return parse_clue(submission)
    elif type == 'KILL_COUNT':
        submission.extra = TypeAdapter(KillCountExtra).validate_python(submission.extra)
        return parse_kill_count(submission)
    elif type == 'COMBAT_ACHIEVEMENT':
        submission.extra = TypeAdapter(CombatAchievementExtra).validate_python(submission.extra)
        return parse_combat_achievement(submission)
    elif type == 'PET':
        submission.extra = TypeAdapter(PetExtra).validate_python(submission.extra)
        return parse_pet(submission)
    elif type == 'SPEEDRUN':
        submission.extra = TypeAdapter(SpeedrunExtra).validate_python(submission.extra)
        return parse_speedrun(submission)
    elif type == 'BARBARIAN_ASSAULT_GAMBLE':
        submission.extra = TypeAdapter(BAGambleExtra).validate_python(submission.extra)
        return parse_barbarian_assault_gamble(submission)
    elif type == 'PLAYER_KILL':
        submission.extra = TypeAdapter(PlayerKillExtra).validate_python(submission.extra)
        return parse_player_kill(submission)
    elif type == 'GROUP_STORAGE':
        submission.extra = TypeAdapter(GroupStorageExtra).validate_python(submission.extra)
        return parse_group_storage(submission)
    elif type == 'GRAND_EXCHANGE':
        submission.extra = TypeAdapter(GrandExchangeExtra).validate_python(submission.extra)
        return parse_grand_exchange(submission)
    elif type == 'TRADE':
        submission.extra = TypeAdapter(PlayerTradeExtra).validate_python(submission.extra)
        return parse_trade(submission)
    elif type == 'LEAGUES_AREA':
        submission.extra = TypeAdapter(LeaguesAreaExtra).validate_python(submission.extra)
        return parse_leagues_area(submission)
    elif type == 'LEAGUES_RELIC':
        submission.extra = TypeAdapter(LeaguesRelicExtra).validate_python(submission.extra)
        return parse_leagues_relic(submission)
    elif type == 'LEAGUES_TASK':
        submission.extra = TypeAdapter(LeaguesTaskExtra).validate_python(submission.extra)
        return parse_leagues_task(submission)
    elif type == 'CHAT':
        submission.extra = TypeAdapter(ChatExtra).validate_python(submission.extra)
        return parse_chat(submission)
    elif type == 'LOGIN':
        submission.extra = TypeAdapter(ExternalPluginExtra).validate_python(submission.extra)
        return parse_login(submission)
    else:
        print(f"Unknown type: {type}")

    return {}

async def parse_dink_request(payload_json: str, file: bytes) -> None:
    # generate an id for this request
    id = uuid.uuid4()
    print(f"Request received: {str(id)}")
    image_required = False
    file_content = file  # Store file content in memory
    if payload_json:
        try:
            result = parse_json_data(payload_json)
            if result:
                image_required = True
        except Exception as e:
            logging.error(f"Error parsing request ({str(id)}): {e}")
            logging.error(json.dumps(payload_json, indent=2))
    if file_content and image_required:
        # Save the image to memory
        with open("lootImage.png", "wb") as f:
            f.write(file_content)
    print(f"Request parsed successfully: {str(id)}")
