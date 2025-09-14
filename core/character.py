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

    def _item_mod(self, key):
        total = 0
        seen = set()
        for item in self.equipped_items.values():
            if item and id(item) not in seen:
                mods = item.get("modifiers", {})
                total += mods.get(key, 0)
                seen.add(id(item))
        return total

    @property
    def effective_damage(self):
        return super().effective_damage + self._item_mod("damage")

    @property
    def effective_draw_count(self):
        return super().effective_draw_count + self._item_mod("draws")

    @property
    def effective_defence(self):
        return super().effective_defence + self._item_mod("defence")

    @property
    def effective_physical_resistance(self):
        return super().effective_physical_resistance + self._item_mod("physical_resistance")

    @property
    def effective_magical_resistance(self):
        return super().effective_magical_resistance + self._item_mod("magical_resistance")

    @property
    def effective_max_health(self):
        return super().effective_max_health + self._item_mod("max_health")

    @property
    def effective_mana_retention(self):
        return super().effective_mana_retention + self._item_mod("mana_retention")

# Equipment & Progression:

    def unequip_item(self, item):
        slots_to_clear = item.get("slot") if isinstance(item, dict) else getattr(item, "slot", None)
        if not slots_to_clear:
            return False
        for slot in slots_to_clear:
            self.equipped_items[slot] = None
        self.apply_item_effects(item, equipping=False)
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
        self.apply_item_effects(item, equipping=True)
        self.remove_from_inventory(item)
        return True
    
    def apply_item_effects(self, item, equipping=True):
        effects_data = item.get("effects", {})
        for effect_type, effect_list in effects_data.items():
            for effect_name in effect_list:
                effect_data = {
                    "type": effect_type.rstrip('s'),  # "on_hit_effects" -> "on_hit_effect"
                    "effect_name": effect_name,
                    "source": item["name"]
                }
                if equipping:
                    self.active_effects.add_effect(effect_data)
                else:
                    # Find and remove matching effect
                    matching_effects = [
                        e for e in self.active_effects.active_effects
                        if (e.get("type") == effect_data["type"] and 
                            e.get("effect_name") == effect_name and
                            e.get("source") == item["name"])
                    ]
                    for effect in matching_effects:
                        self.active_effects.remove_effect(effect)
        
        
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