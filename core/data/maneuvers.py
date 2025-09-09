# core/maneuvers.py

MANEUVERS = {
    "parry": {
        "name": "Parry",
        "type": "defensive",
        "description": "Use your weapon to block an incoming attack.",
        "cost": 1,
        "effect": "defence",
    },
    "riposte": {
        "name": "Riposte",
        "type": "offensive",
        "description": "A quick counter-attack after a successful parry.",
        "cost": 1,
        "effect": "counter_attack",
        "requires": "parry",
    },
    "dodge": {
        "name": "Dodge",
        "type": "defensive",
        "description": "Evade an incoming attack, avoiding damage entirely.",
        "cost": 1,
        "effect": "defence",
    },
    "cleave": {
        "name": "Cleave",
        "type": "offensive",
        "description": "A powerful attack that can hit multiple enemies in front of you.",
        "cost": 2,
    },
    "block": {
        "name": "Block",
        "type": "defensive",
        "description": "Raise your shield to block incoming attacks, reducing damage taken.",
        "cost": 1,
        "effect": "defence",
    },
    "brace": {
        "name": "Brace",
        "type": "defensive",
        "description": "Brace yourself with a heavy shield, greatly reducing damage taken but limiting mobility.",
        "cost": 1,
        "effect": "physical_resistance",
    },
    "bulwark": {
        "name": "Bulwark",
        "type": "defensive",
        "description": "Adopt a defensive stance, allowing your armour to effectively protect against damage",
        "cost": 1,
        "effect": "physical_resistance",
    },
    "channel": {
        "name": "Channel",
        "type": "utility",
        "description": "Conventrate to channel mana into spells, but at the cost of martial awareness.",
        "cost": 1,
        "effect": "mana_gain",
    },
}   