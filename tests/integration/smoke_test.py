# python
# tests/integration/smoke_test.py

# To run the test:
# uv run -m tests.integration.smoke_test 

from core.character import Character
from core.data.equipment import WEAPONS, ARMOUR

# --- Spells ---
class Spell:
    def __init__(self, name, cost, fn, desc=""):
        self.name, self.cost, self.fn, self.desc = name, cost, fn, desc

def spell_firebolt(caster, target):
    dmg = max(0, 3 - target.effective_magical_resistance)
    previous_health = target.current_health
    target.lose_health(dmg)
    return f"{caster.name} casts Firebolt for {dmg} magic damage. ({previous_health}/{target.effective_max_health} -> {target.current_health}/{target.effective_max_health})"

def spell_minor_heal(caster, target):
    target = caster
    amt = 3
    previous_health = target.current_health
    target.gain_health(amt)
    return f"{caster.name} casts Minor Healing, restoring {amt} HP. ({previous_health}/{target.effective_max_health} -> {target.current_health}/{target.effective_max_health})"

def spell_curse(caster, target):
    target.beadbag.add_bead("green", "temporary")
    target.beadbag.add_bead("green", "temporary")
    return f"{caster.name} casts Curse, adding two temporary green beads to {target.name}."

def spell_cleanse(caster, target):
    temps = [b for b in caster.drawbag.beads_in_bag if b.get("permanence") == "temporary"]
    if not temps:
        return f"{caster.name} casts Cleanse, but nothing to remove."
    removed = 0
    for bead in temps:
        caster.drawbag.return_bead(bead)
        removed += 1
    caster.drawbag.draw_bead(amount=removed)
    collect_resources_from_draw(caster)
    return f"{caster.name} casts Cleanse, removes {removed} temp bead(s) and redraws."

def available_spells_table():
    return {
        "firebolt": Spell("Firebolt", 1, spell_firebolt, "Flat magic damage (3)."),
        "minor_heal": Spell("Minor Healing", 1, spell_minor_heal, "Heal 3 HP."),
        "curse": Spell("Curse", 1, spell_curse, "Add two temporary green beads to enemy."),
        "cleanse": Spell("Cleanse", 1, spell_cleanse, "Remove all temp beads in draw and redraw."),
    }

# --- Helpers ---
def collect_resources_from_draw(actor):
    # Blue beads give mana per your defaults
    for bead in actor.drawbag.beads_in_bag:
        rule = actor.get_bead_rules(bead)
        if rule.get("resource") == "mana":
            actor.gain_mana(1)

def seed_demo_loadout(entity, enemy=False):
    # Replace a few black-permanent with blue-permanent for mana
    to_replace = 3 if not enemy else 2
    while to_replace > 0 and entity.beadbag.remove_bead_by_type("black", "permanent"):
        entity.beadbag.add_bead("blue", "permanent")
        to_replace -= 1
    entity.draw_count += 2
    entity.modify_bead_rule("blue", is_success=True, resource="mana")

    entity.damage = 2 # if not enemy else 1

def initial_draw_and_resources(actor):
    actor.drawbag.beads_in_bag.clear()
    actor.draw_beads(draw_count=actor.effective_draw_count)
    collect_resources_from_draw(actor)
    potential_bonus = [0]
    for bead in actor.drawbag.beads_in_bag:
        rule = actor.get_bead_rules(bead)
        effects = rule.get('effects', [])
        for effect in effects:
            if effect == 'critical_success':
                potential_bonus[0] += 1
            elif effect == 'critical_failure':
                potential_bonus[0] -= 1
    base_successes = actor.count_successes()
    drawn = [b["color"] + ("(temp)" if b["permanence"] != "permanent" else "") 
             for b in actor.drawbag.beads_in_bag]
    total_projected_successes = base_successes + potential_bonus[0]
    print(f"Drawn beads: {drawn}")
    print(f"Successes: {total_projected_successes} | Mana: {actor.current_mana}")

def choose_loadout():    
    loadouts = {
            1: {
                "name": "Scout",
                "description": "Light armor + hand axe - mobile with bleed effects",
                "items": [WEAPONS["hand_axe"], ARMOUR["light_armour"], ARMOUR["light_shield"]],
                "preferred_spell": "curse" 
            },
            2: {
                "name": "Knight", 
                "description": "Shield + sword - balanced offense/defense with parry",
                "items": [WEAPONS["short_sword"], ARMOUR["light_shield"], ARMOUR["medium_armour"]],
                "preferred_spell": "minor_heal" 
            },
            3: {
                "name": "Berserker",
                "description": "Two-handed axe - high damage with cleave potential", 
                "items": [WEAPONS["two_handed_axe"], ARMOUR["medium_armour"]],
                "preferred_spell": "firebolt"  
            }
        }
    for num, loadout in loadouts.items():
        print(f"{num}. {loadout['name']} - {loadout['description']}")
    while True:
        try:
            choice=int(input("Enter choice (1-3): "))
            if choice in loadouts:
                return loadouts[choice]
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Please enter a number.")

def apply_loadout(entity, loadout, enemy=False):
    for item in loadout["items"]:
        entity.add_to_inventory(item)
        entity.equip_item(item)
    if enemy == True:
        entity.preferred_spell = loadout.get("preferred_spell", None)



def basic_attack(attacker, defender):
    bonus_successes = [0]
    for bead in attacker.drawbag.beads_in_bag:
        attacker.apply_bead_effect(bead, bonus_successes)
    total_successes = attacker.count_successes() + bonus_successes[0]
    if total_successes > defender.effective_defence:
        attacker.resolve_hit(defender)
        return f"{attacker.name} hits for {attacker.effective_damage - defender.effective_physical_resistance} physical."
    return f"{attacker.name} misses."

def consume_mana(caster, cost):
    if caster.current_mana < cost:
        return False
    caster.current_mana -= cost
    return True

def choose_spell_input(spells, caster):
    if not spells:
        return None
    spell_list = list(spells.values())
    print("\nAvailable Spells:")
    for i, spell in enumerate(spell_list, 1):
        print(f"{i}. {spell.name} (Cost: {spell.cost}) - {spell.desc}")
    choice = input("cast a spell? Enter the number, or blank to skip:  ").strip()
    if not choice:
        return None 
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(spell_list):
            return spell_list[idx]
        else:
            print("Invalid choice.")
            return None
        
    except ValueError:
        print("Please enter a valid number.")
        return None

def end_of_turn_cleanup(actor):
    actor.drawbag.resolve_draw(clear_persist=False)  # temp beads removed; persistent/permanent handled
    actor.reset_mana()

def enemy_turn(enemy, player, spells):
    initial_draw_and_resources(enemy)
    messages = []
    spell = spells[enemy.preferred_spell] if enemy.preferred_spell in spells else spells["firebolt"]
    if enemy.current_mana >= spell.cost and consume_mana(enemy, spell.cost):
        messages.append(spell.fn(enemy, player))
    messages.append(basic_attack(enemy, player))
    end_of_turn_cleanup(enemy)
    return "\n".join(messages)

# --- Main loop ---
def run_battle(player, enemy):
    spells = available_spells_table()
    round_num = 1
    while player.is_alive() and enemy.is_alive():
        print("\n" + "-" * 60)
        print(f"Round {round_num}")
        print(player)
        print(enemy)

        initial_draw_and_resources(player)
        print(f"Drawn: {len(player.drawbag.beads_in_bag)} | Successes: {player.count_successes()} | Mana: {player.current_mana}")

        used_spells = set()
        while player.current_mana > 0:
            available_spells = {}
            for spell_key, spell_obj in spells.items():
                if spell_obj.name not in used_spells and spell_obj.cost <= player.current_mana:
                    available_spells[spell_key] = spell_obj
            if not available_spells:
                print("No more spells available this turn.")
                break
            spell = choose_spell_input(available_spells, player)
            if not spell:
                print("Skipping spell casting.")
                break
            if consume_mana(player, spell.cost):
                print(spell.fn(player, enemy))
                used_spells.add(spell.name)
                print(f"Remaining mana: {player.current_mana}")
            else:
                print(f"Not enough mana to cast {spell.name}.")
                break
            
        print(basic_attack(player, enemy))
        end_of_turn_cleanup(player)

        if not enemy.is_alive():
            break

        print(enemy_turn(enemy, player, spells))
        if not player.is_alive():
            break
        
        input("Press Enter to proceed to the next round...")
        round_num += 1

    print("\nBattle Over!")
    print("You win!" if not enemy.is_alive() else "You were defeated...")

def main():
    hero = Character("Hero", race_name="Human")
    dummy = Character("Dummy", race_name="Human")
    print("Choose your loadout: ")
    hero_loadout = choose_loadout()
    apply_loadout(hero, hero_loadout, enemy=False)
    print("Choose your enemy's loadout: ")
    enemy_loadout = choose_loadout()
    apply_loadout(dummy, enemy_loadout, enemy=True)
    seed_demo_loadout(hero, enemy=False)
    seed_demo_loadout(dummy, enemy=True)
    run_battle(hero, dummy)

if __name__ == "__main__":
    main()