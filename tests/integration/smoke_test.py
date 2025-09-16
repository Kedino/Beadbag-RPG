# python
# tests/integration/smoke_test.py

# To run the test:
# uv run -m tests.integration.smoke_test 

from core.character import Character
from core.data.equipment import WEAPONS, ARMOUR
from core.data.maneuvers import MANEUVERS

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
    new_beads = []
    for bead in temps:
        new_beads.extend(caster.drawbag.redraw_bead(bead))
    for bead in new_beads:
        caster.apply_resource_effect(bead)
    return f"{caster.name} casts Cleanse, removes {len(temps)} temp bead(s) and redraws."

def available_spells_table():
    return {
        "firebolt": Spell("Firebolt", 1, spell_firebolt, "Flat magic damage (3)."),
        "minor_heal": Spell("Minor Healing", 1, spell_minor_heal, "Heal 3 HP."),
        "curse": Spell("Curse", 1, spell_curse, "Add two temporary green beads to enemy."),
        "cleanse": Spell("Cleanse", 1, spell_cleanse, "Remove all temp beads in draw and redraw."),
    }

def available_spells(spell_table, used, player):
    return {
        k: v for k, v in spell_table.items()
        if v.name not in used and v.cost <= player.current_mana
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
    entity.base_draw_count += 2
    entity.modify_bead_rule("blue", is_success=True, resource="mana")

    entity.base_damage = 2 # if not enemy else 1

def initial_draw_and_resources(actor, round_num, enemy):
    actor.drawbag.beads_in_bag.clear()
    actor.active_effects.progress_effects()
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
    actor.expected_successes = total_projected_successes
    actor.spent_successes = 0
    print_round_information(round_num, actor, enemy)
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
                "items": [WEAPONS["short_sword"], ARMOUR["heavy_shield"], ARMOUR["medium_armour"]],
                "preferred_spell": "minor_heal" 
            },
            3: {
                "name": "Berserker",
                "description": "Two-handed hammer - high damage and stun potential", 
                "items": [WEAPONS["two_handed_hammer"], ARMOUR["medium_armour"]],
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

def choose_maneuver_input(manager):
    options = manager.get_available_maneuvers()
    if not options:
        print("No maneuvers available.")
        return None
    print("\nAvailable Maneuvers:")
    for i, name in enumerate(options, 1):
        m = MANEUVERS[name]
        print(f"{i}. {m['name']} (Cost: {m.get('cost',0)}) - {m.get('description','')}")
    choice = input("Use a maneuver? Enter number, or blank to skip: ").strip()
    if not choice:
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except ValueError:
        pass
    print("Invalid choice.")
    return None

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
    actor.maneuver_manager.reset_maneuvers()

def enemy_turn(enemy, player, spells, round_num):
    initial_draw_and_resources(enemy, round_num, player) 
    messages = []
    spell = spells[enemy.preferred_spell] if enemy.preferred_spell in spells else spells["firebolt"]
    if enemy.current_mana >= spell.cost and consume_mana(enemy, spell.cost):
        messages.append(spell.fn(enemy, player))
    messages.append(basic_attack(enemy, player))
    end_of_turn_cleanup(enemy)
    return "\n".join(messages)

def print_combat_summary(entity):
    parts = str(entity).split(" | ")
    # Expect: [Name, (HP ...), [Def ...], Mana..., Draw..., Damage..., Effects...]
    core = [parts[0], parts[1], parts[2], parts[4], parts[5]]  # pick what you want
    print(" | ".join(core))

def print_details(entity):
    print(entity)  # full repr

# --- Main loop ---
def run_battle(player, enemy):
    spells = available_spells_table()
    round_num = 1
    while player.is_alive() and enemy.is_alive():
        initial_draw_and_resources(player, round_num, enemy)

        action_menu(player, enemy, available_spells_table())

        if not enemy.is_alive():
            break

        print(enemy_turn(enemy, player, spells, round_num))
        if not player.is_alive():
            break
        
        input("Press Enter to proceed to the next round...")
        round_num += 1

    print("\nBattle Over!")
    print("You win!" if not enemy.is_alive() else "You were defeated...")

def print_round_information(round_num, player, enemy):
    print("\n" + "-" * 60)
    print(f"Round {round_num}")
    print_combat_summary(player)
    print("\n")
    print_combat_summary(enemy)
    print("\n")

def action_menu(player, enemy, spells):
    used_spells = set()
    while True:
        print("\nChoose Action:")
        print("1. Perform maneuver")
        print("2. Cast spell")
        print("3. Show combattant details")
        print("4. Resolve attack and end turn")
        choice = input("Choose an action (1-4): ").strip()

        if choice == "1":
            name = choose_maneuver_input(player.maneuver_manager)
            if not name:
                continue
            ok, reason = player.maneuver_manager.perform_maneuver(name, target=enemy)
            if ok:
                print(f"Used maneuver: {MANEUVERS[name]['name']}")
                print(f"Projected successes left: {player.expected_successes - player.spent_successes}")
            else:
                print(f"Cannot use {name}: {reason}")
            
        elif choice == '2':
            available = available_spells(spells, used_spells, player)
            if not available:
                print("No spells available to cast.")
                continue
            spell = choose_spell_input(available, player)
            if not spell:
                continue
            if consume_mana(player, spell.cost):
                print(spell.fn(player, enemy))
                used_spells.add(spell.name)
                print(f"Remaining mana: {player.current_mana}")
            else:
                print(f"Not enough mana to cast {spell.name}.")

        elif choice == '3':
            print_details(player)
            print_details(enemy)

        elif choice == '4':
            print(basic_attack(player, enemy))
            end_of_turn_cleanup(player)
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

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