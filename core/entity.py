# core/entity.py

from core.effect_manager import EffectManager

class Entity():
    def __init__(self, name, defence=1, physical_resistance=0, magical_resistance=0, health=10):
        self.name = name
        self.base_defence = defence if defence is not None else 1
        self.base_physical_resistance = physical_resistance if physical_resistance is not None else 0
        self.base_magical_resistance = magical_resistance if magical_resistance is not None else 0
        self.base_max_health = health if health is not None else 10
        self.current_health = self.base_max_health
        self.active_effects = EffectManager()


    def _mod(self, key):
        value = self.active_effects.get_modifier(key)
        return 0 if value is None else value

    @property
    def effective_defence(self):
        return self.base_defence + self._mod("defence")

    @property
    def effective_physical_resistance(self):
        return self.base_physical_resistance + self._mod("physical_resistance")

    @property
    def effective_magical_resistance(self):
        return self.base_magical_resistance + self._mod("magical_resistance")

    @property
    def effective_max_health(self):
        return self.base_max_health + self._mod("max_health")

    def change_health(self, amount):
        prev_alive = self.is_alive()
        self.current_health = max(0, min(self.effective_max_health, self.current_health + amount))
        if prev_alive and not self.is_alive(): 
            self.die()

    def die(self):
        pass

    def gain_health(self, amount):
        self.change_health(abs(amount))
    def lose_health(self, amount):
        self.change_health(-abs(amount))

    def increase_max_health(self, amount):
        self.base_max_health += amount
    def decrease_max_health(self, amount):
        self.base_max_health = max(0, self.base_max_health - amount)
        if self.current_health > self.base_max_health:
            self.current_health = self.base_max_health
    
    def gain_physical_resistance(self, amount):
        self.base_physical_resistance += amount
    def lose_physical_resistance(self, amount):
        self.base_physical_resistance -= amount
    def gain_magical_resistance(self, amount):
        self.base_magical_resistance += amount
    def lose_magical_resistance(self, amount):
        self.base_magical_resistance -= amount

    def gain_defence(self, amount):
        self.base_defence += amount
    def lose_defence(self, amount):
        self.base_defence = max(0, self.base_defence - amount)

    def is_alive(self):
        return self.current_health > 0
    
    def __repr__(self):
        parts = [
            self.name,
            f"(HP: {self.current_health}/{self.effective_max_health})",
            f"[Def: {self.effective_defence}, P.Res: {self.effective_physical_resistance}, M.Res: {self.effective_magical_resistance}]"
        ]
        effects = self.active_effects.list_active_effects()
        if effects:
            effect_summaries = [effect.get("type", "effect") for effect in effects]
            parts.append(f"Effects: {', '.join(effect_summaries)}")
        return " | ".join(parts)

    
