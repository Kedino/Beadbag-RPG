# core/entity.py

class Entity():
    def __init__(self, name, defence=1, physical_resistance=0, magical_resistance=0, health=10):
        self.name = name
        self.base_defence = defence
        self.base_physical_resistance = physical_resistance
        self.base_magical_resistance = magical_resistance
        self.current_health = health
        self.base_max_health = health
        self.active_effects = []

    @property
    def effective_defence(self):
        return self.base_defence
    
    @property
    def effective_physical_resistance(self):
        return self.base_physical_resistance
    
    @property
    def effective_magical_resistance(self):
        return self.base_magical_resistance 
    
    @property
    def effective_max_health(self):
        return self.base_max_health

    def change_health(self, amount):
        prev_alive = self.is_alive()
        self.current_health = max(0, min(self.effective_max_health, self.current_health + amount))
        if prev_alive and not self.is_alive(): 
            self.die()

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
    
    def add_effect(self, effect):
        if effect not in self.active_effects:
            self.active_effects.append(effect)
    def remove_effect(self, effect):
        if effect in self.active_effects:
            self.active_effects.remove(effect)

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
        if self.active_effects:
            #Here we will later add code to represent active effects
            pass
        return " | ".join(parts)

    
