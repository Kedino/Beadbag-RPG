

def bead_effect_degen(entity, amount=1):
    entity.lose_health(amount)

def bead_effect_heal(entity, amount=1):
    entity.gain_health(amount)



EFFECT_MAP = {
    "degen": bead_effect_degen,
    "heal": bead_effect_heal,
    # ...and more as needed
}
