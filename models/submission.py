from pydantic import BaseModel
from models.notification_models import DeathExtra, CollectionExtra, LevelExtra, XPMilestoneExtra, LootExtra, SlayerExtra, QuestExtra, ClueExtra, KillCountExtra, CombatAchievementExtra, AchievementDiaryExtra, PetExtra, SpeedrunExtra, BAGambleExtra, PlayerKillExtra, GroupStorageExtra, GrandExchangeExtra, PlayerTradeExtra, LeaguesAreaExtra, LeaguesMasteryExtra, LeaguesRelicExtra, LeaguesTaskExtra, ChatExtra, ExternalPluginExtra, MetadataExtra

class DiscordUser(BaseModel):
    id: str
    name: str
    avatarHash: str

class Submission(BaseModel):
    type: str
    playerName: str
    accountType: str
    dinkAccountHash: str
    clanName: str | None = None
    groupIronClanName: str | None = None
    seasonalWorld: bool
    world: int | None = None
    regionId: int | None = None
    extra: DeathExtra | CollectionExtra | LevelExtra | XPMilestoneExtra | LootExtra | SlayerExtra | QuestExtra | ClueExtra | KillCountExtra | CombatAchievementExtra | AchievementDiaryExtra | PetExtra | SpeedrunExtra | BAGambleExtra | PlayerKillExtra | GroupStorageExtra | GrandExchangeExtra | PlayerTradeExtra | LeaguesAreaExtra | LeaguesMasteryExtra | LeaguesRelicExtra | LeaguesTaskExtra | ChatExtra | ExternalPluginExtra | MetadataExtra
    discordUser: DiscordUser | None = None
    content: str
    embeds: list