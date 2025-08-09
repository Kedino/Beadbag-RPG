# core/bead_effects.py

def bead_effect_degen(entity, amount=1):
    entity.lose_health(amount)

def bead_effect_heal(entity, amount=1):
    entity.gain_health(amount)

def bead_effect_critical_success(entity, amount=1):
    entity.current_successes += amount

def bead_effect_critical_failure(entity, amount=1):
    entity.current_successes -= amount

def bead_effect_vulnerability(entity, amount=1):
    entity.effective_physical_resistance -= amount
    entity.effective_magical_resistance -= amount

def bead_effect_resilience(entity, amount=1):
    entity.effective_physical_resistance += amount
    entity.effective_magical_resistance += amount



EFFECT_MAP = {
    "degen": bead_effect_degen,
    "heal": bead_effect_heal,
    "critical_success": bead_effect_critical_success,
    "critical_failure": bead_effect_critical_failure,
    "vulnerability": bead_effect_vulnerability,
    "resilience": bead_effect_resilience,
    # ...add more as needed
}
