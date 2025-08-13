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
        self.equipped_items = {"main_hand": None,
                               "off_hand": None,
                               "armour": None,
        }

      
    def initialise_starting_beads(self, success_count=10, failure_count=10):
        for _ in range(success_count):
            self.beadbag.add_bead('white', 'permanent')
        for _ in range(failure_count):
            self.beadbag.add_bead('black', 'permanent')
        

#Equipment & Progression:

    def unequip_item(self, item):
        slots_to_clear = item.get("slot") if isinstance(item, dict) else getattr(item, "slot", None)
        if not slots_to_clear:
            return False
        for slot in slots_to_clear:
            self.equipped_items[slot] = None
        self.add_to_inventory(item)
        return True

    def equip_item(self, item):
        if item not in self.inventory:
            return False
        slots = item.get("slot") if isinstance(item, dict) else getattr(item, "slot", None)
        if not slots or not isinstance(slots, list):
            return False
        for slot in slots:
            currently_equipped = self.equipped_items.get(slot)
            if currently_equipped:
               self.unequip_item(currently_equipped)
            self.equipped_items[slot] = item
        self.remove_from_inventory(item)
        return True
        
        
    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def has_item(self, item):
        return item in self.inventory
    
    def list_items(self, type=None):
        if type is None:
            return list(self.inventory)
        return [
            item for item in self.inventory 
            if getattr(item, "type", None) == type 
            or (isinstance(item, dict) and item.get("type", None) == type)
            ]
        
    def add_training(self, skill):
        """Learn new skill/training"""