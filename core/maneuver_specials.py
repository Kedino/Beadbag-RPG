# core/maneuver_specials.py

def sp_gain_resource(actor, target=None, *, resource, amount=1, **_):
    add = getattr(actor, f"gain_{resource}", None)
    if callable(add):
        add(amount)

def sp_add_beads(actor, target=None, *, who="self", color, permanence="temporary", count=1, **_):
    entity = actor if who == "self" else (target or actor)
    for _ in range(count):
        entity.beadbag.add_bead(color, permanence)

SPECIALS_MAP = {
    "gain_resource": sp_gain_resource,
    "add_beads": sp_add_beads,
}