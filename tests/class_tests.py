from core.entity_base_stats import Entity
from core.beadbag import Beadbag, Drawbag
from core.bead_effects import EFFECT_MAP
from core.actor import Actor
from core.character import Character

test_cases = [
    {
        "Test": "Entity creation and __repr__",
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
        "run": False # Set to True to run this test
    },
    {
        "Test": "Actor creation and __repr__",
        "Class": Actor,
        "test_args": [
            ("Black Bear", 5, 1, 1, 30, 0, 6),
            ("Goblin", 3, 0, 0, 8, 0, 5)
        ],
        "Expected Output": [
            ("Black Bear | (HP: 30/30) | [Def: 5, P.Res: 1, M.Res: 1] | Mana: 0 | Draw Count: 6 | Damage: 1"),
            ("Goblin | (HP: 8/8) | [Def: 3, P.Res: 0, M.Res: 0] | Mana: 0 | Draw Count: 5 | Damage: 1")
        ],
        "run": True # Set to True to run this test
    },
    {
        "Test": "Character creation and __repr__",
        "Class": Character,
        "test_args": [
            ("")
        ],
        "Expected Output": [
            ("")
        ],
        "run": False # Set to True to run this test
    },
    {
        "Test": "Beadbag methods",
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
        "run": True # Set to True to run this test
    },
    {
        "Test": "Beadbag should_be_removed logic",
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
        "run": True # Set to True to run this test
    }
]

def run_tests():
    total_tests = 0
    passed_tests = 0

    for test_group in test_cases:
        if not test_group.get("run", True): 
            print(f"--- Skipping {test_group['Test']} ---")
            print()
            continue 

        print(f"--- Testing {test_group['Test']} ---")

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
                expected_state = action_test["expected_state"]
                try:
                    action_method = getattr(entity, method_to_call)
                    action_method(*method_args)
                    state_check_method = getattr(entity, state_check_method_name)
                    output_state = state_check_method()
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