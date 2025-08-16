# tests/class_tests.py

from core.entity import Entity
from core.beadbag import Beadbag, Drawbag
from core.bead_effects import EFFECT_MAP
from core.actor import Actor
from core.character import Character
from .test_config import TEST_CONFIG
from core.data.equipment import WEAPONS, ARMOUR

two_handed_sword = WEAPONS["two_handed_sword"]
sword = WEAPONS["short_sword"]


# =======================================================================
#                           TEST CASE MANUAL
# =======================================================================
# Each key in ALL_TESTS is a test name. Its value is a dictionary
# that defines the test.
# Run tests from the root using "uv run -m tests.class_tests"
#
# --- Optional Keys ---
# "status": Use this key to mark a test with a special status.
#           - "incomplete": The test will be skipped with an INFO message.
#           - If the "status" key is omitted, the test is considered
#             normal and active.
#
# --- Test Types ---
# 1. Creation Test: Checks __repr__ after creating an object.
#    Requires keys: "Class", "test_args", "Expected Output"
#
# 2. Action Test: Performs actions on an object and checks its state.
#    Requires keys: "Class", "creation_args", "action_tests"
#    Optional "check_return_value": True for methods that return a value.
#
# 3. Function Test: Tests a simple, stateless method.
#    Requires keys: "Class", "function_tests"
#
# --- Test selection ---
# Tests are selected basedin the TEST_CONFIG dictionary, located in test_config.py
# Tests that are set to False in TEST_CONFIG will be skipped.
# Tests that are set to True will be executed.
# If a test is not present in TEST_CONFIG, it will be skipped.
# The TEST_CONFIG dictionary is updated by the update_test_config.py script.
# 
# =======================================================================


ALL_TESTS = {
    "Entity creation and __repr__": {
        "Class": Entity,
        "test_args": [
            ("Tree", 1, 1, 0, 10),
            ("Iron door", 2, 3, 1, 20),
            ("Apple", 3, 0, 0, 1)
        ],
        "Expected Output": [
            ("Tree | (HP: 10/10) | [Def: 1, P.Res: 1, M.Res: 0]"),
            ("Iron door | (HP: 20/20) | [Def: 2, P.Res: 3, M.Res: 1]"),
            ("Apple | (HP: 1/1) | [Def: 3, P.Res: 0, M.Res: 0]")
        ],            
    },
    "Actor creation and __repr__": {
        "Class": Actor,
        "test_args": [
            ("Black Bear", 5, 1, 1, 30, 0, 6),
            ("Goblin", 3, 0, 0, 8, 0, 5)
        ],
        "Expected Output": [
            ("Black Bear | (HP: 30/30) | [Def: 5, P.Res: 1, M.Res: 1] | Mana: 0 | Draw Count: 6 | Damage: 1"),
            ("Goblin | (HP: 8/8) | [Def: 3, P.Res: 0, M.Res: 0] | Mana: 0 | Draw Count: 5 | Damage: 1")
        ],
    },
    "Character creation and __repr__": {
        "Class": Character,
        "test_args": [
            ("Dwarf", "Dwarf", 2, 0, 0, 12, 0, 5),
            ("Elf", "Elf", 1, 0, 1, 10, 1, 6),
        ],
        "Expected Output": [
            ("Dwarf | (HP: 12/12) | [Def: 2, P.Res: 0, M.Res: 0] | Mana: 0 | Draw Count: 5 | Damage: 1 | Race: Dwarf"),
            ("Elf | (HP: 10/10) | [Def: 1, P.Res: 0, M.Res: 1] | Mana: 0 | Draw Count: 6 | Damage: 1 | Race: Elf"),
        ],
    },
    "Equip and unequip items in Character": {
        "Class": Character,
        "creation_args": ("TestCharacter", "Human", 1, 0, 0, 10, 0, 5),
        "action_tests": [
            {
                "method_to_call": "add_to_inventory",
                "method_args": two_handed_sword,
                "state_check_method": "has_item",
                "state_check_args": (two_handed_sword,),
                "expected_state": True
            },
            {
                "method_to_call": "equip_item",
                "method_args": (two_handed_sword,),
                "state_check_method": "list_equipped_items",
                "expected_state": [two_handed_sword]
            },
            {
                "method_to_call": "remove_from_inventory",
                "method_args": (two_handed_sword,),
                "check_return_value": True,
                "expected_state": False
            },
            {
                "method_to_call": "add_to_inventory",
                "method_args": (sword,),
                "state_check_method": "has_item",
                "state_check_args": (sword,),
                "expected_state": True
            },
            {
                "method_to_call": "add_to_inventory",
                "method_args": sword,
                "state_check_method": "has_item",
                "state_check_args": (sword,),
                "expected_state": True
            },
            {
                "method_to_call": "equip_item",
                "method_args": (sword,),
                "state_check_method": "list_equipped_items",
                "expected_state": [sword]
            },
            {
                "method_to_call": "unequip_item",
                "method_args": (sword,),
                "state_check_method": "list_equipped_items",
                "expected_state": []
            },
            {
                "method_to_call": "remove_from_inventory",
                "method_args": (sword,),
                "state_check_method": "list_items",
                "expected_state": (two_handed_sword)
            },
        ],
    },
    "Beadbag methods": {
        "Class": Beadbag,
        "Creation_args": (),
        "Action_tests": [
            {
                "method_to_call": "add_bead",
                "method_args": ("white", "permanent"),
                "state_check_method": "get_bead_summary",
                "expected_state": {('white', 'permanent'): 1},
            },
            {
                "method_to_call": "add_bead",
                "method_args": ("black", "temporary"),
                "state_check_method": "get_bead_summary",
                "expected_state": {('white', 'permanent'): 1, ('black', 'temporary'): 1},
            },
            {
                "method_to_call": "remove_bead",
                "method_args": ({'color': 'white', 'permanence': 'permanent'},),
                "state_check_method": "get_bead_summary",
                "expected_state": {('black', 'temporary'): 1},
            },
            {
                "method_to_call": "list_beads",
                "method_args": (),
                "state_check_method": "list_beads",
                "expected_state": [{'color': 'black', 'permanence': 'temporary'}],
            }
        ],
    },
    "Beadbag should_be_removed logic": {
        "Class": Beadbag, 
        "function_tests": [
            {
                "method_to_test": "should_be_removed",
                "args": (
                    Beadbag(), 
                    {'permanence': 'temporary'},
                ),
                "expected_result": True
            },
            {
                "method_to_test": "should_be_removed",
                "args": (
                    Beadbag(),
                    {'permanence': 'persistent'},
                    False
                ),
                "expected_result": False
            },
            {
                "method_to_test": "should_be_removed",
                "args": (
                    Beadbag(),
                    {'permanence': 'persistent'},
                    True
                ),
                "expected_result": True
            },
            {
                "method_to_test": "should_be_removed",
                "args": (
                    Beadbag(),
                    {'permanence': 'permanent'}
                ),
                "expected_result": False
            },
        ],
    }
}

def run_tests():
    total_tests = 0
    passed_tests = 0

    for test_name, test_group in ALL_TESTS.items():
        if test_group.get("status") == "incomplete":
            print(f"--- INFO: Skipping incomplete test: {test_name} ---")
            print()
            continue

        if not TEST_CONFIG.get(test_name, False):
            print(f"--- Skipping {test_name} ---")
            print()
            continue 

        print(f"--- Testing {test_name} ---")

        class_to_test = test_group["Class"]
        if "Expected Output" in test_group:
            test_args = test_group["test_args"]
            expected_output = test_group["Expected Output"]

            for test_num, (args, expected) in enumerate(zip(test_args, expected_output), 1):
                total_tests += 1
                entity = class_to_test(*args)
                output = repr(entity)

                try:
                    assert output == expected
                    passed_tests += 1
                    print(f"Test {test_num}: Passed")
                except AssertionError:
                    print(f"Test {test_num}: Failed")
                    print(f"  {'Expected:':<10} {expected}")
                    print(f"  {'Got:':<10} {output}")
            print()
        
        elif "Action_tests" in test_group:
            entity = class_to_test(*test_group["Creation_args"])
            action_tests = test_group["Action_tests"]

            for i, action_test in enumerate(action_tests, 1):
                total_tests += 1

                method_to_call = action_test["method_to_call"]
                method_args = action_test["method_args"]
                state_check_method_name = action_test["state_check_method"]
                state_check_args = action_test.get("state_check_args", ())
                expected_state = action_test["expected_state"]
                check_return_value = action_test.get("check_return_value", False)
                try:
                    action_method = getattr(entity, method_to_call)
                    result = action_method(*method_args)
                    if check_return_value:
                        assert result == expected_state
                    else:
                        state_check_method = getattr(entity, state_check_method_name)
                        output_state = state_check_method(*state_check_args)
                        assert output_state == expected_state
                    passed_tests += 1
                    print(f"Action Test: {method_to_call} - Passed")
                except AssertionError:
                    print(f"Action Test: {method_to_call} - Failed")
                    print(f"  {'Expected state:':<20} {expected_state}")
                    print(f"  {'Actual state:':<20} {output_state}")
            print()

        elif "function_tests" in test_group:
            function_tests = test_group["function_tests"]
            
            for i, function_test in enumerate(function_tests, 1):
                total_tests += 1

                method_to_call = function_test["method_to_test"]
                args = function_test["args"]
                expected_result = function_test["expected_result"]

                try:
                    method = getattr(class_to_test, method_to_call)
                    result = method(*args)
                    assert result == expected_result
                    passed_tests += 1
                    print(f"Function Test {i}: {method_to_call} - Passed")
                except AssertionError:
                    print(f"Function Test {i}: {method_to_call} - Failed")
                    print(f"  {'Expected:':<10} {expected_result}")
                    print(f"  {'Got:':<10} {result}")
            print()
        
        print("--- Test summary ---")
        print(f"[{passed_tests}/{total_tests}] tests passed.")
        print()


if __name__ == "__main__":
    run_tests()
    print("All tests completed.")