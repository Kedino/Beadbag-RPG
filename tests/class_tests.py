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
        "run": True # Runs the tests when set to True
    },
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
    
    print("--- Test summary ---")
    print(f"[{passed_tests}/{total_tests}] tests passed.")


if __name__ == "__main__":
    run_tests()
    print("All tests completed.")