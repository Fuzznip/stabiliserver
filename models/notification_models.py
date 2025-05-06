from pydantic import BaseModel

# Shared Models
class Item(BaseModel):
    id: int
    quantity: int
    priceEach: int
    name: str
    criteria: list[str] | None = None
    rarity: float | None = None

class Location(BaseModel):
    regionId: int
    plane: int
    instanced: bool

# Death Models
class DeathExtra(BaseModel):
    valueLost: int
    isPvp: bool
    killerName: str | None = None
    killerNpcId: int | None = None
    keptItems: list[Item]
    lostItems: list[Item]
    location: Location

# Collection Models
class CollectionExtra(BaseModel):
    itemName: str
    itemId: int
    price: int
    completedEntries: int
    totalEntries: int
    currentRank: str
    rankProgress: int
    logsNeededForNextRank: int
    nextRank: str
    justCompletedRank: str
    dropperName: str | None = None
    dropperType: str | None = None
    dropperKillCount: int | None = None

# Level Models
class CombatLevel(BaseModel):
    value: int
    increased: bool

class LevelExtra(BaseModel):
    levelledSkills: dict[str, int]
    allSkills: dict[str, int]
    combatLevel: CombatLevel | None = None

class XPMilestoneExtra(BaseModel):
    xpData: dict[str, int]
    milestoneAchieved: list[str]
    interval: int

# Loot Models
class LootExtra(BaseModel):
    items: list[Item]
    source: str
    party: list[str] | None = None
    category: str | None = None
    killCount: int | None = None
    rarestProbability: float | None = None
    npcId: int | None = None

# Slayer Models
class SlayerExtra(BaseModel):
    slayerTask: str
    slayerCompleted: int
    slayerPoints: int
    killCount: int
    monster: str

# Quest Models
class QuestExtra(BaseModel):
    questName: str
    completedQuests: int
    totalQuests: int
    questPoints: int
    totalQuestPoints: int

# Clue Models
class ClueExtra(BaseModel):
    clueType: str
    numberCompleted: int
    items: list[Item]

# Kill Count Models
class KillCountExtra(BaseModel):
    boss: str
    count: int
    gameMessage: str
    time: str | None = None
    isPersonalBest: bool | None = None
    personalBest: str | None = None
    party: list[str] | None = None

# Combat Achievement Models
class CombatAchievementExtra(BaseModel):
    tier: str
    task: str
    taskPoints: int
    totalPoints: int
    tierProgress: int
    tierTotalPoints: int
    totalPossiblePoints: int
    currentTier: str | None = None
    nextTier: str | None = None
    justCompletedTier: str | None = None

# Achievement Diary Models
class AchievementDiaryExtra(BaseModel):
    area: str
    difficulty: str
    total: int
    tasksCompleted: int
    tasksTotal: int
    areaTasksCompleted: int
    areaTasksTotal: int

# Pet Models
class PetExtra(BaseModel):
    petName: str
    milestone: str | None = None
    duplicate: bool | None = None

# Speedrunning Models
class SpeedrunExtra(BaseModel):
    questName: str
    personalBest: str | None = None
    currentTime: str
    isPersonalBest: bool | None = None

# Barbarian Assault Models
class BAGambleExtra(BaseModel):
    gambleCount: int
    items: list[Item]

# Player Kill Models
class EquipmentItem(BaseModel):
    id: int
    priceEach: int
    name: str

class Equipment(BaseModel):
    AMULET: EquipmentItem | None = None
    WEAPON: EquipmentItem | None = None
    TORSO: EquipmentItem | None = None
    LEGS: EquipmentItem | None = None
    HANDS: EquipmentItem | None = None

class PlayerKillExtra(BaseModel):
    victimName: str
    victimCombatLevel: int
    victimEquipment: Equipment
    world: int | None = None
    location: Location | None = None
    myHitpoints: int
    myLastDamage: int

# Group Storage Models
class GroupStorageExtra(BaseModel):
    groupName: str
    deposits: list[Item]
    withdrawals: list[Item]
    netValue: int

# Grand Exchange Models
class GEItem(BaseModel):
    id: int
    quantity: int
    priceEach: int
    name: str

class GrandExchangeExtra(BaseModel):
    slot: int
    status: str
    item: GEItem
    marketPrice: int
    targetPrice: int
    targetQuantity: int
    sellerTax: int

# Player Trade Models
class PlayerTradeExtra(BaseModel):
    counterparty: str
    receivedItems: list[Item]
    givenItems: list[Item]
    receivedValue: int
    givenValue: int

# Leagues Models
class LeaguesAreaExtra(BaseModel):
    area: str
    index: int
    tasksCompleted: int
    tasksUntilNextArea: int

class LeaguesMasteryExtra(BaseModel):
    masteryType: str
    masteryTier: int

class LeaguesRelicExtra(BaseModel):
    relic: str
    tier: int
    requiredPoints: int
    totalPoints: int
    pointsUntilNextTier: int

class LeaguesTaskExtra(BaseModel):
    taskName: str
    difficulty: str
    taskPoints: int
    totalPoints: int
    tasksCompleted: int
    tasksUntilNextArea: int | None = None
    pointsUntilNextRelic: int | None = None
    pointsUntilNextTrophy: int | None = None
    earnedTrophy: str | None = None

# Chat Models
class ChatExtra(BaseModel):
    type: str
    message: str
    source: str | None = None
    clanTitle: dict[str, str] | None = None

# External Plugin Models
class ExternalPluginExtra(BaseModel):
    sourcePlugin: str
    metadata: dict[str, str] | None = None

# Metadata Models
class MetadataExtra(BaseModel):
    world: int
    collectionLog: dict[str, int] | None = None
    combatAchievementPoints: dict[str, int] | None = None
    achievementDiary: dict[str, int] | None = None
    achievementDiaryTasks: dict[str, int] | None = None
    barbarianAssault: dict[str, int] | None = None
    skills: dict[str, dict[str, int]] | None = None
    questCount: dict[str, int] | None = None
    questPoints: dict[str, int] | None = None
    slayer: dict[str, int] | None = None
    pets: list[dict[str, str]] | None = None
