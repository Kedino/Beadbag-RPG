from entity_base_stats import Entity
from beadbag import Beadbag, Drawbag

class ActionMechanics(Entity):
    def __init__(self, name, defence=2, physical_resistance=0, magical_resistance=0, health=10):
        super().__init__(name, defence, physical_resistance, magical_resistance, health)
        
        self.beadbag = Beadbag()
        self.drawbag = Drawbag(self.beadbag)
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
        
    def initialise_starting_beads(self, success_count=12, failure_count=8):
        for _ in range(success_count):
            self.beadbag.add_bead('white', 'permanent')
        for _ in range(failure_count):
            self.beadbag.add_bead('black', 'permanent')
        
