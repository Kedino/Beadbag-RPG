# core/data/default_bead_definitions.py

BEAD_DEFINITIONS = {
    "white": {'is_success': True, 'resource': None, 'effects': [], "event": None},
    "black": {'is_success': False, 'resource': None, 'effects': [], "event": None},
    "gold": {'is_success': True, 'resource': None, 'effects': ['critical_success'], "event": None},
    "grey": {'is_success': False, 'resource': None, 'effects': ['critical_failure'], "event": None},
    "blue": {'is_success': False, 'resource': "mana", 'effects': [], "event": None},
    "brown": {'is_success': False, 'resource': None, 'effects': ['resilience'], "event": None},
    "purple": {'is_success': False, 'resource': None, 'effects': [], "event": True},
    "green": {'is_success': False, 'resource': None, 'effects': ['degen'], "event": None},
    "red": {'is_success': False, 'resource': None, 'effects': ['heal'], "event": None},
    # Add more bead definitions as needed
}