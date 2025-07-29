from .beadbag import Beadbag, Drawbag
from .entity_base_stats import Entity
from action_mechanics import ActionMechanics

class Character(ActionMechanics):
    def __init__(self, name, defence=None, physical_resistance=None, magical_resistance=None, health=None, draw_count=None, mana_retention=None):
        super().__init__(name, defence, physical_resistance, magical_resistance, health, draw_count, mana_retention)
        
        self.race = None
        self.training = []

        self.inventory = []
        self.equipped_items = {}
      
    def initialise_starting_beads(self, success_count=10, failure_count=10):
        for _ in range(success_count):
            self.beadbag.add_bead('white', 'permanent')
        for _ in range(failure_count):
            self.beadbag.add_bead('black', 'permanent')
        

#Equipment & Progression:

    def equip_item(self, item, slot):
        """Equip an item to a slot"""
        
    def add_to_inventory(self, item):
        """Add item to inventory"""
        
    def add_training(self, skill):
        """Learn new skill/training"""