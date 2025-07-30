

def bead_effect_degen(entity, amount=1):
    entity.lose_health(amount)

def bead_effect_heal(entity, amount=1):
    entity.gain_health(amount)

def bead_effect_critical_success(entity, amount=1):
    entity.current_successes += amount

def bead_effect_critical_failure(entity, amount=1):
    entity.current_successes -= amount



EFFECT_MAP = {
    "degen": bead_effect_degen,
    "heal": bead_effect_heal,
    "critical_success": bead_effect_critical_success,
    "critical_failure": bead_effect_critical_failure,
    # ...add more as needed
}
