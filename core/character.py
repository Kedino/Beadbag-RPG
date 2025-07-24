from .beadbag import Beadbag

class Character():
    def __init__(self, name, defence=2, physical_resistance=0, magical_resistance=0, health=10, draw_count=5):
        self.name = name
        self.defence = defence
        self.physical_resistance = physical_resistance
        self.magical_resistance = magical_resistance
        self.health = health
        self.max_health = health
        self.draw_count = draw_count
        self.active_effects = []

        self.race = None
        self.training = []

        self.inventory = []
        self.equipped_items = {}

        self.beadbag = BeadBag()
        self.initialise_starting_beads()

        self.bead_rules = {
            'white': {'is_success': True, 'effects': []},
            'black': {'is_success': False, 'effects': []},
        }


    def modify_bead_rule(self, color, is_success=None, add_effects=None):
        if color not in self.bead_rules:
            self.bead_rules[color] = {'is_success': False, 'effects': []}
        if is_success is not None:
            self.bead_rules[color]['is_success'] = is_success
        if add_effects:
            if not isinstance(add_effects, list):
                add_effects = [add_effects]
            self.bead_rules[color]['effects'].extend(add_effects)
        
    def initialise_starting_beads(self, success_count=10, failure_count=10):
        for _ in range(success_count):
            self.beadbag.add_bead('white', 'permanent')
        for _ in range(failure_count):
            self.beadbag.add_bead('black', 'permanent')
        
#Bead Drawing & Action Resolution:

    def draw_beads(self, count=None):
        """Draw beads for an action (uses self.draw_count if not specified)"""
        
    def resolve_action(self, target=None, action_type='attack'):
        """Full action: draw beads, apply effects, determine success/failure"""
        
    def count_successes(self, drawn_beads):
        """Count successes based on bead_rules"""
        
    def apply_bead_effects(self, drawn_beads):
        """Process all the effects from drawn beads"""

#Health & Damage:

    def take_damage(self, amount, damage_type='physical'):
        """Apply damage with armor reduction"""
        
    def heal(self, amount):
        """Restore health (capped at max_health)"""
        
    def is_alive(self):
        """Check if character is still alive"""

#Effects Management:

    def add_effect(self, effect):
        """Add temporary effect"""
        
    def remove_effect(self, effect_name):
        """Remove specific effect"""
        
    def process_effects(self):
        """Apply all active effects (call each turn)"""

#Equipment & Progression:

    def equip_item(self, item, slot):
        """Equip an item to a slot"""
        
    def add_to_inventory(self, item):
        """Add item to inventory"""
        
    def add_training(self, skill):
        """Learn new skill/training"""