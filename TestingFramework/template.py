"""
Testing Genie - Template File
Copy this file to get started quickly with your own tests
"""

from testing_genie import TestingGenie


# ============================================================================
# Define Your Test Functions Here
# ============================================================================

def test_example_1():
    """
    Replace this with your first test.
    Test functions should:
    - Accept no parameters
    - Return a value (optional)
    - Raise an exception if the test fails
    """
    # Your test code here
    result = 2 + 2
    assert result == 4, "Expected 4"
    return result


def test_example_2():
    """Replace this with your second test"""
    # Your test code here
    data = [1, 2, 3, 4, 5]
    assert sum(data) == 15
    return sum(data)


def test_example_3():
    """Replace this with your third test"""
    # Your test code here
    text = "Hello World"
    assert len(text) > 0
    return text.upper()


# ============================================================================
# Main Test Execution
# ============================================================================

if __name__ == "__main__":
    # Initialize Testing Genie with your config file
    genie = TestingGenie('config.ini')
    
    # Register your tests
    # Syntax: genie.register_test('test_name', test_function)
    genie.register_test('test_example_1', test_example_1)
    genie.register_test('test_example_2', test_example_2)
    genie.register_test('test_example_3', test_example_3)
    
    # Run all tests
    print("\nRunning all tests...\n")
    genie.run_all_tests()
    
    # Display results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    # Print detailed summary
    genie.print_summary()
    
    # Print comparison table
    genie.print_comparison()
    
    # Optional: Export results to JSON
    genie.export_results('my_test_results.json')
    
    print("\n✓ Testing complete!")
    print("Check 'my_test_results.json' for detailed results")


# ============================================================================
# Tips:
# ============================================================================
# 
# 1. Configure test runs in config.ini:
#    [DEFAULT]
#    runs = 5
#    
#    [test_example_1]
#    runs = 10
#
# 2. Run specific tests:
#    genie.run_test('test_example_1', runs=20)
#
# 3. Get statistics for a specific test:
#    stats = genie.get_stats('test_example_1')
#    print(f"Success rate: {stats.success_rate}%")
#
# 4. Compare specific tests:
#    genie.print_comparison(['test_example_1', 'test_example_2'])
#
# 5. Clear results and re-run:
#    genie.clear_results()
#    genie.run_all_tests()
#
