# core/data/effects.py

EFFECTS = {
    "physical_vulnerability": {
        "type": "vulnerability",
        "modifiers": {"physical_resistance": -1},
        "duration": 1,
    },
    "magical_vulnerability": {
        "type": "vulnerability",
        "modifiers": {"magical_resistance": -1},
        "duration": 1,
    },
    "physical_resilience": {
        "type": "resilience",
        "modifiers": {"physical_resistance": 1},
        "duration": 1,
    },
    "magical_resilience": {
        "type": "resilience",
        "modifiers": {"magical_resistance": 1},
        "duration": 1,
    },
    'defence': {
        "type": "defence",
        "modifiers": {"defence": 1},
        "duration": 1,
    },
    'damage': {
        "type": "damage",
        "modifiers": {"damage": 1},
        "duration": 1,
    },
    'draw_count': {
        "type": "draw_count",
        "modifiers": {"draw_count": 1},
        "duration": 1,
    },
}