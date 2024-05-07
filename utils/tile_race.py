import db

tile = {
  "name": "name",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "",
      "count": 1,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "",
      "count": 1,
      "points": 1,
    }
  ]
}

raid_tile = {
  "name": "Raid!",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Avernic defender hilt, Ghrazi rapier, Sanguinesti staff (uncharged), Justiciar faceguard, Justiciar legguards, Scythe of vitur (uncharged)",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Dexterous prayer scroll, Arcane prayer scroll, Twisted buckler, Dragon hunter crossbow, Ancestral hat, Ancestral robe top, Ancestral robe bottom, Dinh's bulwark, Dragon claws, Elder maul, Kodai insignia, Twisted bow",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Lightbearer, Osmumten's fang, Elidinis' ward, Masori mask, Masori body, Masori chaps, Tumeken's shadow (uncharged)",
      "count": 1,
      "points": 1,
    },
    {
      "type": "KC",
      "trigger": "Tombs of Amascut, Chambers of Xeric, Theatre of Blood",
      "count": 25,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "KC",
      "trigger": "Giant Mole",
      "count": 125,
      "points": 1,
    }
  ]
}

wilderness_tile = {
  "name": "Wilderness Bosses",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Dragon pickaxe:Callisto, Dragon pickaxe:Artio, Dragon pickaxe:Vet'ion, Dragon pickaxe:Calvar'ion, Dragon pickaxe:Venenatis, Dragon pickaxe:Spindel",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Voidwaker hilt, Voidwaker gem, Voidwaker blade",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Fangs of venenatis, Skull of vet'ion, Claws of callisto",
      "count": 1,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Fedora",
      "count": 1,
      "points": 4,
    }
  ]
}

dks_tile = {
  "name": "The Triumvirate",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Berserker ring, Warrior ring, Seers ring, Archers ring",
      "count": 3,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Ancient page 1, Ancient page 2, Ancient page 3, Ancient page 4",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Bandos page 1, Bandos page 2, Bandos page 3, Bandos page 4",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Saradomin page 1, Saradomin page 2, Saradomin page 3, Saradomin page 4",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Guthix page 1, Guthix page 2, Guthix page 3, Guthix page 4",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Zamorak page 1, Zamorak page 2, Zamorak page 3, Zamorak page 4",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Armadyl page 1, Armadyl page 2, Armadyl page 3, Armadyl page 4",
      "count": 1,
      "points": 1,
    },
  ]
}

gotr_tile = {
  "name": "Guardians of the Rift",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Abyssal pearl",
      "count": 150,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Catalytic talisman, Abyssal needle, Abyssal lantern, Abyssal red dye, Abyssal green dye, Abyssal blue dye",
      "count": 1,
      "points": 2,
    },
  ]
}

super_slayer_tile = {
  "name": "Super Slayer",
  "main_triggers": [
    {
      "type": "XP",
      "trigger": "Slayer",
      "count": 400000,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Slayer's enchantment",
      "count": 1,
      "points": 2,
    },
  ]
}

dt2_tile = {
  "name": "Desert Treasure II",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Awakener's orb",
      "count": 2,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Virtus mask, Virtus robe top, Virtus robe bottom",
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Leviathan's lure, Siren's staff, Executioner's axe head, Eye of the duke",
      "count": 1,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "CHAT",
      "trigger": "Agility Pyramid",
      "count": 25,
      "points": 1,
    },
  ]
}

gauntlet_tile = {
  "name": "The Gauntlet",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Crystal shard:The Gauntlet",
      "count": 300,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Crystal armour seed, Crystal weapon seed, Enhanced crystal weapon seed",
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "CHAT",
      "trigger": "Agility Arena Ticket",
      "count": 50,
      "points": 1,
    }
  ]
}

zulrah_tile = {
  "name": "Super Snake",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Tanzanite fang, Magic fang, Serpentine visage, Uncut onyx, Tanzanite mutagen, Magma mutagen",
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "KC",
      "trigger": "Scurrius",
      "count": 50,
      "points": 1,
    }
  ]
}

vorkath_tile = {
  "name": "Money Dragon",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Vorkath's head",
      "count": 2,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": "Skeletal visage, Jar of decay, Draconic visage, Bonecrusher necklace",
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Scaly blue dragonhide",
      "count": 1,
      "points": 1,
    }
  ]
}

free_tile = {
  "name": "FREE!",
  "main_triggers": [],
  "side_triggers": []
}

clue_tile = {
  "name": "Confounding Clues",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Ranger boots, Holy sandals, Wizard boots, Spiked manacles, Climbing boots (g)",
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Purple sweets",
      "count": 20,
      "points": 1,
    }
  ]
}

tempoross_tile = {
  "name": "Tempoross",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "",
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Spirit flakes",
      "count": 200,
      "points": 1,
    }
  ]
}

demonic_gorilla_tile = {
  "name": "Money Monkeys",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Zenyte shard, Ballista limbs",
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": "Dragon javelin heads",
      "count": 125,
      "points": 1,
    }
  ]
}

muspah_tile = {
  "name": "Phantom of the Muspah",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": "Venator shard",
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "CHAT",
      "trigger": "Sword completed in: [0-9]*m* *[0-9]+s at quality: ([0-9]+)",
      "count": 2000,
      "points": 1,
    }
  ]
}

toa_tile = {
  "name": "Tombs of Amongus",
  
}

tob_tile = {
  "name": "Theatre of Bussy",
  
}

tzhaar_tile = {
  "name": "Trouble in TzHaar Town",
  
}

colosseum_tile = {
  "name": "Down with Dizana",
  
}

cox_tile = {
  "name": "Chambers of Xeric",
  

}

gwd_tile = {
  "name": "God Wars Dungeon",
  
}

mop_tile = {
  "name": "Moons of Peril",
  

}

tiles = [
  raid_tile,
  wilderness_tile,
  dks_tile,
  gotr_tile,
  super_slayer_tile,
  dt2_tile,
  gauntlet_tile,
  zulrah_tile,
  vorkath_tile,
  free_tile,
  clue_tile,
  tempoross_tile,
  demonic_gorilla_tile,
  muspah_tile,
  toa_tile,
  tob_tile,
  tzhaar_tile,
  colosseum_tile,
  cox_tile,
  gwd_tile,
  mop_tile
]


