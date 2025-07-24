from .beadbag import Beadbag, Drawbag
from .entity_base_stats import Entity
from action_mechanics import ActionMechanics

class Character(ActionMechanics):
    def __init__(self, name, defence=2, physical_resistance=0, magical_resistance=0, health=10, draw_count=5):
        super().__init__(name, defence, physical_resistance, magical_resistance, health)
        self.draw_count = draw_count
        
        self.race = None
        self.training = []

        self.inventory = []
        self.equipped_items = {}
      
    def initialise_starting_beads(self, success_count=10, failure_count=10):
        for _ in range(success_count):
            self.beadbag.add_bead('white', 'permanent')
        for _ in range(failure_count):
            self.beadbag.add_bead('black', 'permanent')
        
#Bead Drawing & Action Resolution:

    def draw_beads(self, draw_count=None):
        if draw_count is None:
            draw_count = self.draw_count
        drawn_beads = self.drawbag.draw_bead(amount=draw_count)
        return drawn_beads
        
    def resolve_action(self, target=None, action_type='attack'):
        """Full action: draw beads, apply effects, determine success/failure"""
        
    def count_successes(self):
        count = 0
        for bead in self.drawbag.beads_in_bag:
            rule = self.bead_rules.get(bead['color'], {})
            if rule.get('is_success'):
                count += 1
        return count
        
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