# core/maneuver_manager.py

import copy
from core.data.maneuvers import MANEUVERS
from core.data.effects import EFFECTS
from core.maneuver_specials import SPECIALS_MAP

class ManeuverManager:
    def __init__(self, actor):
        self.actor = actor
        self.used_groups = set()

    def enabled_maneuver_groups(self):
        groups = set()
        items = getattr(self.actor, "equipped_items", None)
        if items:
            for item in items.values():
                if not item:
                    continue
                for group in item.get("maneuvers", []):
                    groups.add(group)
        for group in getattr(self.actor, "maneuver_groups", []):
            groups.add(group)
        return groups

    def get_available_maneuvers(self):
        enabled = self.enabled_maneuver_groups()
        available = []
        for maneuver_name in enabled:
            m = MANEUVERS.get(maneuver_name)
            if not m:
                continue
            group = m.get("group", maneuver_name)
            if group not in self.used_groups:
                available.append(maneuver_name)
        return available
    
    def can_perform(self, name):
        m = MANEUVERS.get(name)
        if not m:
            return False, "unknown_maneuver"
        group = m.get("group", name)
        if group in self.used_groups:
            return False, "group_used"
        if self.actor.spent_successes + m.get("cost", 0) > self.actor.expected_successes:
            return False, "not_enough_successes"
        if name not in self.enabled_base_names():
            return False, "not_enabled_by_equipment"
        return True, None


    def perform_maneuver(self, name, target=None):
        ok, reason = self.can_perform(name)
        if not ok:
            return False, reason
        m = MANEUVERS[name]
        self.actor.spent_successes += m.get("cost", 0)
        for eff in m.get("effects", []):
            if eff in EFFECTS:
                self.actor.active_effects.add_effect(copy.deepcopy(EFFECTS[eff]))
        for spec in m.get("special", []):
            self._apply_special(spec, target)
        self.used_groups.add(m.get("group", name))
        return True, None

    def _apply_special(self, spec_name, target):
        result = spec_name.get("result")
        func = SPECIALS_MAP.get(result)
        if callable(func):
            func(self.actor, target, **spec_name)

    def reset_maneuvers(self):
        self.used_groups.clear()