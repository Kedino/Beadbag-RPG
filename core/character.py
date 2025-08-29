# core/character.py

from .beadbag import Beadbag, Drawbag
from .entity import Entity
from .actor import Actor
from core.bead_effects import EFFECT_MAP
from .data.races import RACES

class Character(Actor):
    def __init__(self, name, race_name="Human", defence=None, physical_resistance=None, magical_resistance=None, health=None, mana_retention=None, draw_count=None):
        super().__init__(name, defence, physical_resistance, magical_resistance, health, mana_retention, draw_count)
        
        self.race = None
        race_data = RACES.get(race_name.lower())
        if race_data:
            self.race = race_data["name"]
            for stat_to_modify, bonus in race_data['stats_modifiers'].items():
                current_value = getattr(self, stat_to_modify)
                setattr(self, stat_to_modify, current_value + bonus)
            for starting_bead in race_data['starting_beads']:
                bead_color, bead_type = starting_bead
                self.beadbag.add_bead(bead_color, bead_type)

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
        
    @property
    def effective_defence(self):
        total = super().effective_defence
        for item in self.equipped_items.values():
            if item:
                total += item.get("modifiers", {}).get("defence", 0)
        return total
    
    @property
    def effective_physical_resistance(self):
        total = super().effective_physical_resistance
        for item in self.equipped_items.values():
            if item:
                total += item.get("modifiers", {}).get("physical_resistance", 0)
        return total
    
    @property
    def effective_magical_resistance(self):
        total = super().effective_magical_resistance
        for item in self.equipped_items.values():
            if item:
                total += item.get("modifiers", {}).get("magical_resistance", 0)
        return total
    
    @property
    def effective_max_health(self):
        total = super().effective_max_health
        for item in self.equipped_items.values():
            if item:
                total += item.get("modifiers", {}).get("max_health", 0)
        return total
    
    @property
    def effective_mana_retention(self):
        total = super().effective_mana_retention
        for item in self.equipped_items.values():
            if item:
                total += item.get("modifiers", {}).get("mana_retention", 0)
        return total

    @property
    def effective_damage(self):
        total = super().effective_damage
        for item in self.equipped_items.values():
            if item:
                total += item.get("modifiers", {}).get("damage", 0)
        return total
    
    @property
    def effective_draw_count(self):
        total = super().effective_draw_count
        for item in self.equipped_items.values():
            if item:
                total += item.get("modifiers", {}).get("draws", 0)
        return total

# Equipment & Progression:

    def unequip_item(self, item):
        slots_to_clear = item.get("slot") if isinstance(item, dict) else getattr(item, "slot", None)
        if not slots_to_clear:
            return False
        for slot in slots_to_clear:
            self.equipped_items[slot] = None
        if "equipped_effect" in item:
            self.active_effects.remove_effect(item["equipped_effect"])
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
        if "equipped_effect" in item:
            self.active_effects.add_effect(item["equipped_effect"])
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
    
# Training & Skills:

    def add_training(self, skill):
        """Learn new skill/training"""

# repr
    def __repr__(self):
        base = super().__repr__()
        parts = [base]
        if hasattr(self, "race") and self.race:
            parts.append(f"Race: {self.race}")
        if hasattr(self, "equipped_items") and self.equipped_items:
            equipped = [
                f"{slot.capitalize()}: {item['name']}" 
                for slot, item in self.equipped_items.items() if item
            ]
            if equipped:
                parts.append("Equipped: " + ", ".join(equipped))
        if hasattr(self, "training") and self.training:
        # Add code for training here
            pass
        return " | ".join(parts)