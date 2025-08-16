# core/data/effects.py

EFFECTS = {
    "vulnerability": {
        "type": "vulnerability",
        "modifiers": {"physical_resistance": -1, "magical_resistance": -1},
        "duration": 1,
    },
    "resilience": {
        "type": "resilience",
        "modifiers": {"physical_resistance": 1, "magical_resistance": 1},
        "duration": 1,
    },
}