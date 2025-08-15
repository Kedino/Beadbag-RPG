# core/actor.py

from .entity import Entity
from .beadbag import Beadbag, Drawbag
from core.bead_effects import EFFECT_MAP
from .data.default_bead_definitions import BEAD_DEFINITIONS
from .effect_manager import EffectManager


class Actor(Entity):
    def __init__(self, name, defence=1, physical_resistance=None, magical_resistance=None, health=None, mana_retention=None, draw_count=5):
        super().__init__(name, defence, physical_resistance, magical_resistance, health)
        self.mana_retention = mana_retention if mana_retention is not None else 0
        self.current_mana = 0
        self.damage = 1

        self.draw_count = draw_count
        
        self.beadbag = Beadbag()
        self.drawbag = Drawbag(self.beadbag)
        self.initialise_starting_beads()
        self.active_effects = EffectManager()

        self.bead_rules = {
            'white': {'is_success': True, 'resource': None, 'effects': [], "event": None},
            'black': {'is_success': False, 'resource': None, 'effects': []}, "event": None,
        }

        self.event_queue = []

    @property
    def effective_defence(self):
        total = super().effective_defence
        total += self.active_effects.get_modifier("defence")
        return total
    
    @property
    def effective_physical_resistance(self):
        total = super().effective_physical_resistance
        total += self.active_effects.get_modifier("physical_resistance")
        return total
    
    @property
    def effective_magical_resistance(self):
        total = super().effective_magical_resistance
        total += self.active_effects.get_modifier("magical_resistance")
        return total
    
    @property
    def effective_max_health(self):
        total = super().effective_max_health
        total += self.active_effects.get_modifier("max_health")
        return total
    
    @property
    def effective_mana_retention(self):
        total = self.mana_retention
        total += self.active_effects.get_modifier("mana_retention")
        return total

    @property
    def effective_damage(self):
        total = self.damage
        total += self.active_effects.get_modifier("damage")
        return total
    
    @property
    def effective_draw_count(self):
        total = self.draw_count
        total += self.active_effects.get_modifier("draws")
        return total

    def modify_bead_rule(self, color, is_success=None, resource=None, add_effects=None):
        if color not in self.bead_rules:
            self.bead_rules[color] = {'is_success': False, 'resource': None, 'effects': [], "event": None}
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

    def primary_action(self, target):
        self.initial_draw()
        self.draw_interaction()
        self.resolve_events()
        self.action_resolution(target)
        self.drawbag.resolve_draw(clear_persist=False)

    def initial_draw(self):
        self.drawbag.draw_bead(amount=self.draw_count)
        for bead in self.drawbag.beads_in_bag:
            self.apply_resource_effect(bead)
        
    def draw_interaction(self):
        # Here we will later add code to handle player interactions
        pass

    def resolve_events(self):
        for bead in self.drawbag.beads_in_bag:
            rule = self.get_bead_rules(bead)
            is_event= rule.get('event', None)
            if is_event is True:
                if len(self.event_queue) == 0:
                    continue
                event = self.event_queue.pop(0)
                # Here we would handle any events associated with the bead
                pass

    def action_resolution(self, target):
        self.current_successes = self.count_successes()
        for bead in self.drawbag.beads_in_bag:
            self.apply_bead_effect(bead)
        if self.current_successes > target.effective_defence:
            self.resolve_hit(target)
        
        
    def resolve_hit(self, target):
        damage = self.damage - target.effective_physical_resistance
        if damage < 0:
            damage = 0
        target.lose_health(damage)
        
    def draw_beads(self, draw_count=None):
        if draw_count is None:
            draw_count = self.draw_count
        self.drawbag.draw_bead(amount=draw_count)
    
    def count_successes(self):
        count = 0
        for bead in self.drawbag.beads_in_bag:
            rule = self.get_bead_rules(bead)
            if rule.get('is_success'):
                count += 1
        return count
    
    def get_bead_rules(self, bead):
        if bead["color"] in self.bead_rules:
            return self.bead_rules[bead["color"]]
        else:
            return BEAD_DEFINITIONS.get(bead["color"], {})
       
    def apply_resource_effect(self, bead):
        rule = self.get_bead_rules(bead)
        resource = rule.get('resource', None)
        if resource:
            add_method = getattr(self, f'gain_{resource}', None)
            if callable(add_method):
                add_method(1)

    def apply_bead_effect(self, bead):
        rule = self.get_bead_rules(bead)
        effects = rule.get('effects', [])
        for effect in effects:
            effect_func = EFFECT_MAP.get(effect)
            if callable(effect_func):
                effect_func(self)

    def gain_mana(self, amount):
        self.mana += amount

    def reset_mana(self):
        self.mana = min(self.mana, self.mana_retention)

    def __repr__(self):
        parts = [
            self.name,
            f"(HP: {self.current_health}/{self.effective_max_health})",
            f"[Def: {self.effective_defence}, P.Res: {self.effective_physical_resistance}, M.Res: {self.effective_magical_resistance}]",
            f"Mana: {self.current_mana}",
            f"Draw Count: {self.effective_draw_count}",
            f"Damage: {self.effective_damage}",
        ]
        if hasattr(self, "active_effects") and self.active_effects.list_active_effects():
            effects = self.active_effects.list_active_effects()
            effect_summaries = [e.get("type", "effect") for e in effects]
            parts.append(f"Effects: {', '.join(effect_summaries)}")
        return " | ".join(parts)   
