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
}