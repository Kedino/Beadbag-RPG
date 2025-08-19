# core/bead_effects.py

import copy
from core.data.effects import EFFECTS
from core.effect_manager import EffectManager

def bead_effect_degen(entity, amount=1):
    entity.lose_health(amount)

def bead_effect_heal(entity, amount=1):
    entity.gain_health(amount)

def bead_effect_critical_success(entity, amount=1):
    entity.bonus_successes += amount

def bead_effect_critical_failure(entity, amount=1):
    entity.bonus_successes -= amount

def bead_effect_vulnerability(entity, amount=1):
    effect = copy.deepcopy(EFFECTS["vulnerability"])
    for key in effect["modifiers"]:
        effect["modifiers"][key] *= amount
    entity.active_effects.add_effect(effect)

def bead_effect_resilience(entity, amount=1):
    effect = copy.deepcopy(EFFECTS["resilience"])
    for key in effect["modifiers"]:
        effect["modifiers"][key] *= amount
    entity.active_effects.add_effect(effect)



EFFECT_MAP = {
    "degen": bead_effect_degen,
    "heal": bead_effect_heal,
    "critical_success": bead_effect_critical_success,
    "critical_failure": bead_effect_critical_failure,
    "vulnerability": bead_effect_vulnerability,
    "resilience": bead_effect_resilience,
    # ...add more as needed
}
