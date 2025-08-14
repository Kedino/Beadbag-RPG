# core/effect_manager.py

class EffectManager:
    def __init__(self):
        self.active_effects = []

    def add_effect(self, effect):
        self.active_effects.append(effect)

    def remove_effect(self, effect):
        if effect in self.active_effects:
            self.active_effects.remove(effect)

    def progress_effects(self):
        still_active = []
        for effect in self.active_effects:
            if 'duration' in effect:
                effect["duration"] -= 1
                if effect["duration"] > 0:
                    still_active.append(effect)
            else:
                still_active.append(effect)
        self.active_effects = still_active
    
    def get_modifier(self, modifier_name):
        sum_modifiers = 0
        for effect in self.active_effects:
            mods = effect.get("modifiers", {})
            sum_modifiers += mods.get(modifier_name, 0)
        return sum_modifiers
    
    def list_modifiers(self):
        modifiers = {}
        for effect in self.active_effects:
            for key, value in effect.get('modifiers', {}).items():
                modifiers[key] = modifiers.get(key, 0) + value
        return modifiers
    
    def list_active_effects(self):
        return self.active_effects