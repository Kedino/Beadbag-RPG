# core/equip_effects.py

def on_hit_slash(attacker, target, *args, **kwargs):
    # Extra damage vs lightly armored foes
    if target.effective_physical_resistance <= 1:
        bonus_damage = 2
        target.lose_health(bonus_damage)
        return f"Slash deals {bonus_damage} extra damage to lightly armored foe!"
    return None

def on_hit_bleed(attacker, target, *args, **kwargs):
    # Add temporary degen beads
    target.beadbag.add_bead("green", "temporary")
    return f"Bleed effect applied to {target.name}!"

def on_hit_stun(attacker, target, *args, **kwargs):
    # Add temporary critical failure beads
    target.beadbag.add_bead("black", "temporary")
    return f"{target.name} is stunned!"

def on_hit_pierce(attacker, target, *args, **kwargs):
    # Extra damage vs heavily armored foes
    if target.effective_physical_resistance >= 2:
        bonus_damage = 2
        target.lose_health(bonus_damage)
        return f"Pierce deals {bonus_damage} extra damage to heavily armored foe!"
    return None

def on_hit_heavy_blow(attacker, target, *args, **kwargs):
    # TODO: Implement when block/parry mechanics exist
    pass

def on_hit_knockback(attacker, target, *args, **kwargs):
    # TODO: Implement when movement mechanics exist  
    pass

ON_HIT_EFFECT_MAP = {
    "slash": on_hit_slash,
    "bleed": on_hit_bleed,
    "stun": on_hit_stun,
    "pierce": on_hit_pierce,
    "heavy_blow": on_hit_heavy_blow,  # For two-handed weapons
    "knockback": on_hit_knockback,   # For hammers
}