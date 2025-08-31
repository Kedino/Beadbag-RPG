# core/data/races.py

RACES = {
    "human": {
        "name": "Human",
        "description": "Versatile and adaptable, humans excel in various roles.",
        "stats_modifiers": {},
        "starting_beads": [("gold", "permanent"), ("grey", "permanent")],
        "bead_rules": {
            'gold': {'is_success': True, 'resource': None, 'effects': ['critical_success']},
            'grey': {'is_success': False, 'resource': None, 'effects': ['critical_failure']},
            },
        },
    "elf": {
        "name": "Elf",
        "description": "Graceful and wise, elves have an affinity for the arcane.",
        "stats_modifiers": {},
        "starting_beads": [("blue", "permanent"), ("blue", "permanent")],
        "bead_rules": {
            'blue': {'is_success': False, 'resource': "mana", 'effects': None},
            },
        },
    "dwarf": {
        "name": "Dwarf",
        "description": "Sturdy and resilient, dwarves can take a beating and keep going.",
        "stats_modifiers": {},
        "starting_beads": [("brown", "permanent"), ("brown", "permanent")],
        "bead_rules": {
            'brown': {'is_success': False, 'resource': None, 'effects': ['resilience']},
            },
        },
}   
