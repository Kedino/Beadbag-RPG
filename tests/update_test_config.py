# tests/update_test_config.py

import os
from tests.class_tests import ALL_TESTS
from tests.test_config import TEST_CONFIG

def update_config():
    print("Updating test configuration...")
    
    all_test_names = set(ALL_TESTS.keys())
    configured_tests = set(TEST_CONFIG.keys())
    new_tests = all_test_names - configured_tests
    
    for test_name in new_tests:
        TEST_CONFIG[test_name] = False
        print(f"  + Added new test: '{test_name}'")

    config_file_path = os.path.join('tests', 'test_config.py')
    with open(config_file_path, 'w') as f:
        f.write("# tests/test_config.py\n\n")
        f.write("TEST_CONFIG = {\n")
        for test_name in sorted(TEST_CONFIG.keys()):
            if test_name in all_test_names:
                f.write(f'    "{test_name}": {TEST_CONFIG[test_name]},\n')
        f.write("}\n")
        
    print("...update complete.")

if __name__ == "__main__":
    update_config()