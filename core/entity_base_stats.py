

class Entity():
    def __init__(self, name, defence=1, physical_resistance=0, magical_resistance=0, health=10):
        self.name = name
        self.base_defence = defence
        self.base_physical_resistance = physical_resistance
        self.base_magical_resistance = magical_resistance
        self.health = health
        self.max_health = health
        self.active_effects = []

    def change_health(self, amount):
        self.health = max(0, min(self.max_health, self.health + amount))

    def gain_health(self, amount):
        self.change_health(abs(amount))
    def lose_health(self, amount):
        self.change_health(-abs(amount))

    def increase_max_health(self, amount):
        self.max_health += amount
    def decrease_max_health(self, amount):
        self.max_health = max(0, self.max_health - amount)
        if self.health > self.max_health:
            self.health = self.max_health
    
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
        return self.health > 0


    
