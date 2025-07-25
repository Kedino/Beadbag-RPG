from entity_base_stats import Entity
from beadbag import Beadbag, Drawbag
from core.bead_effects import EFFECT_MAP




class ActionMechanics(Entity):
    def __init__(self, name, defence=2, physical_resistance=None, magical_resistance=None, health=None, mana_retention=None, draw_count=5):
        super().__init__(name, defence, physical_resistance, magical_resistance, health)
        self.mana_retention = mana_retention if mana_retention is not None else 0
        self.mana = 0

        self.draw_count = draw_count
        
        self.beadbag = Beadbag()
        self.drawbag = Drawbag(self.beadbag)
        self.initialise_starting_beads()

        self.bead_rules = {
            'white': {'is_success': True, 'resource': None, 'effects': []},
            'black': {'is_success': False, 'resource': None, 'effects': []},
        }

    def modify_bead_rule(self, color, is_success=None, resource=None, add_effects=None):
        if color not in self.bead_rules:
            self.bead_rules[color] = {'is_success': False, 'resource': None, 'effects': []}
        if is_success is not None:
            self.bead_rules[color]['is_success'] = is_success
        if resource is not None:
            self.bead_rules[color]['resource'] = resource
        if add_effects:
            if not isinstance(add_effects, list):
                add_effects = [add_effects]
            self.bead_rules[color]['effects'].extend(add_effects)
        
    def initialise_starting_beads(self, success_count=12, failure_count=8):
        for _ in range(success_count):
            self.beadbag.add_bead('white', 'permanent')
        for _ in range(failure_count):
            self.beadbag.add_bead('black', 'permanent')
        
    def draw_beads(self, draw_count=None):
        if draw_count is None:
            draw_count = self.draw_count
        self.drawbag.draw_bead(amount=draw_count)
    
    def count_successes(self):
        count = 0
        for bead in self.drawbag.beads_in_bag:
            rule = self.bead_rules.get(bead['color'], {})
            if rule.get('is_success'):
                count += 1
        return count
    
    def apply_resource_effects(self):
        for bead in self.drawbag.beads_in_bag:
            rule = self.bead_rules.get(bead['color'], {})
            resource = rule.get('resource', None)
            if resource:
                add_method = getattr(self, f'gain_{resource}', None)
                if callable(add_method):
                    add_method(1)

    def apply_bead_effects(self):
        for bead in self.drawbag.beads_in_bag:
            rule = self.bead_rules.get(bead['color'], {})
            effects = rule.get('effects', [])
            for effect in effects:
                effect_func = EFFECT_MAP.get(effect)
                if callable(effect_func):
                    effect_func(self)

    def gain_mana(self, amount):
        self.mana += amount

    def reset_mana(self):
        self.mana = min(self.mana, self.mana_retention)

   
