# core/maneuver_manager.py

from core.data.maneuvers import MANEUVERS

class ManeuverManager:
    def __init__(self, actor):
        self.actor = actor
        self.used_maneuvers = set()

    def get_available_maneuvers(self):
        available = []
        for name, details in self.actor.equipped_items.items():
            maneuvers = details.get("maneuvers", []) if details else []
            for maneuver in maneuvers:
                # Add code to get available versions of maneuver from training
                if maneuver not in self.used_maneuvers:
                    available.append(maneuver)
        return available


    def perform_maneuver(self, maneuver_name, target=None):
        maneuver = MANEUVERS.get(maneuver_name)
        self.actor.spent_successes += maneuver.get("cost", 0)
        self.used_maneuvers.add(maneuver_name)
        effects = maneuver.get("effect")
        for effect_name in effects:
            self.actor.active_effects.add_effect(effect_name)


    def reset_maneuvers(self):
        self.used_maneuvers = set()