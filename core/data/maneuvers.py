# core/data/maneuvers.py

MANEUVERS = {
    "parry": {
        "name": "Parry",
        "group": "parry",
        "type": "defensive",
        "description": "Use your weapon to block an incoming attack.",
        "cost": 1,
        "effects": ["defence"],
    },
    "riposte": {
        "name": "Riposte",
        "group": "strike",
        "type": "offensive",
        "description": "A quick counter-attack after a successful parry.",
        "cost": 1,
        "effects": ["counter_attack"],
        "requires": "parry",
    },
    "dodge": {
        "name": "Dodge",
        "group": "dodge",
        "type": "defensive",
        "description": "Evade an incoming attack, avoiding damage entirely.",
        "cost": 1,
        "effects": ["defence"],
    },
    "cleave": {
        "name": "Cleave",
        "group": "strike",
        "type": "offensive",
        "description": "A powerful attack that can hit multiple enemies in front of you.",
        "cost": 2,
    },
    "block": {
        "name": "Block",
        "group": "block",
        "type": "defensive",
        "description": "Raise your shield to block incoming attacks, reducing damage taken.",
        "cost": 1,
        "effects": ["defence"],
    },
    "brace": {
        "name": "Brace",
        "group": "brace",
        "type": "defensive",
        "description": "Brace yourself with a heavy shield, greatly reducing damage taken but limiting mobility.",
        "cost": 1,
        "effects": ["physical_resistance"],
    },
    "bulwark": {
        "name": "Bulwark",
        "group": "bulwark",
        "type": "defensive",
        "description": "Adopt a defensive stance, allowing your armour to effectively protect against damage",
        "cost": 1,
        "effects": ["physical_resistance"],
    },
    "channel": {
        "name": "Channel",
        "group": "channel",
        "type": "utility",
        "description": "Concentrate to channel mana into future turns.",
        "cost": 1,
        "effects": [],
        "special": [
            {"action": "add_beads", "who": "self", "color": "blue", "permanence": "temporary", "count": 2}
        ],
    }
}   