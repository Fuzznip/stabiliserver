from pydantic import BaseModel
from typing import List, Optional

class KillData(BaseModel):
    victim: str
    location: str
    killTime: str
    weapon: Optional[str] = None

class DeathData(BaseModel):
    killer: str
    location: str
    deathTime: str
    weapon: Optional[str] = None

class LootData(BaseModel):
    itemName: str
    quantity: int
    value: int

class LootItem(BaseModel):
    id: int
    quantity: int
    priceEach: int
    name: str
    criteria: List[str]
    rarity: Optional[float] = None

class ExtraFields(BaseModel):
    kills: Optional[List[KillData]] = None
    deaths: Optional[List[DeathData]] = None
    loot: Optional[List[LootData]] = None
    notes: Optional[str] = None
    items: Optional[List[LootItem]] = None
    source: Optional[str] = None
    category: Optional[str] = None
    killCount: Optional[int] = None
    rarestProbability: Optional[float] = None
    npcId: Optional[int] = None
    party: Optional[List[str]] = None
