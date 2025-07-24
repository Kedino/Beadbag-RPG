

class Entity():
    def __init__(self, name, defence=2, physical_resistance=0, magical_resistance=0, health=10):
        self.name = name
        self.defence = defence
        self.physical_resistance = physical_resistance
        self.magical_resistance = magical_resistance
        self.health = health
        self.max_health = health
        self.active_effects = []
