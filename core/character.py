# core/character.py

from .beadbag import Beadbag, Drawbag
from .entity import Entity
from .actor import Actor
from core.bead_effects import EFFECT_MAP
from .data.races import RACES

class Character(Actor):
    def __init__(self, name, race_name="Human", defence=None, physical_resistance=None, magical_resistance=None, health=None, draw_count=None, mana_retention=None):
        super().__init__(name, defence, physical_resistance, magical_resistance, health, draw_count, mana_retention)
        
        self.race = None
        race_data = RACES.get(race_name.lower())
        if race_data:
            self.race = race_data["name"]
            for stat_to_modify, bonus in race_data['stat_modifiers'].items():
                current_value = getattr(self, stat_to_modify)
                setattr(self, stat_to_modify, current_value + bonus)

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