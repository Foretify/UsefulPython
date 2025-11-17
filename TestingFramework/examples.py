"""
Example usage of the Testing Genie framework
This file demonstrates various testing scenarios and use cases
"""

from testing_genie import TestingGenie
import time
import random


# ============================================================================
# Example Test Functions
# ============================================================================

def test_string_operations():
    """Test basic string operations"""
    text = "Hello, Testing Genie!"
    assert len(text) > 0
    assert text.startswith("Hello")
    return text.upper()


def test_list_operations():
    """Test list manipulations"""
    numbers = [1, 2, 3, 4, 5]
    doubled = [x * 2 for x in numbers]
    assert sum(doubled) == 30
    return doubled


def test_dictionary_operations():
    """Test dictionary operations"""
    data = {'a': 1, 'b': 2, 'c': 3}
    assert 'a' in data
    assert data['b'] == 2
    return sum(data.values())


def test_math_operations():
    """Test mathematical calculations"""
    result = sum(range(1, 101))
    assert result == 5050
    return result


def test_fast_computation():
    """Simulate a fast computation"""
    time.sleep(0.001)  # 1ms
    return "Fast"


def test_medium_computation():
    """Simulate a medium-speed computation"""
    time.sleep(0.05)  # 50ms
    return "Medium"


def test_slow_computation():
    """Simulate a slow computation"""
    time.sleep(0.2)  # 200ms
    return "Slow"


def test_variable_performance():
    """Test with variable execution time"""
    sleep_time = random.uniform(0.01, 0.1)
    time.sleep(sleep_time)
    return f"Slept for {sleep_time:.4f}s"


def test_random_failure():
    """Test that randomly fails (20% failure rate)"""
    if random.random() < 0.2:
        raise ValueError("Random failure occurred!")
    return "Success"


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    # Test empty string
    assert len("") == 0
    
    # Test division
    assert 10 / 2 == 5
    
    # Test negative numbers
    assert -5 + 10 == 5
    
    return "All edge cases passed"


def test_data_processing():
    """Simulate data processing task"""
    data = list(range(1000))
    # Filter even numbers
    evens = [x for x in data if x % 2 == 0]
    # Calculate statistics
    avg = sum(evens) / len(evens)
    return f"Processed {len(data)} items, avg: {avg}"


def test_intentional_failure():
    """This test always fails (for demonstration)"""
    raise AssertionError("This test is designed to fail")


# ============================================================================
# Example 1: Basic Usage
# ============================================================================

def example_basic_usage():
    """Demonstrate basic usage of Testing Genie"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    genie = TestingGenie('config.ini')
    
    # Register a few simple tests
    genie.register_test('string_ops', test_string_operations)
    genie.register_test('list_ops', test_list_operations)
    genie.register_test('math_ops', test_math_operations)
    
    # Run all tests
    genie.run_all_tests()
    
    # Print summary
    genie.print_summary()


# ============================================================================
# Example 2: Performance Comparison
# ============================================================================

def example_performance_comparison():
    """Compare performance of different implementations"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Performance Comparison")
    print("="*80)
    
    genie = TestingGenie('config.ini')
    
    # Register tests with different performance characteristics
    genie.register_test('fast_test', test_fast_computation)
    genie.register_test('medium_test', test_medium_computation)
    genie.register_test('slow_test', test_slow_computation)
    
    # Run tests
    genie.run_all_tests()
    
    # Compare performance
    genie.print_comparison()


# ============================================================================
# Example 3: Reliability Testing
# ============================================================================

def example_reliability_testing():
    """Test reliability and failure rates"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Reliability Testing")
    print("="*80)
    
    genie = TestingGenie('config.ini')
    
    # Register tests with different reliability characteristics
    genie.register_test('reliable_test', test_math_operations)
    genie.register_test('flaky_test', test_random_failure)
    
    # Run with many iterations to see failure patterns
    genie.run_test('reliable_test', runs=20)
    genie.run_test('flaky_test', runs=50)
    
    # Print detailed summary
    genie.print_summary()
    
    # Get specific stats
    reliable_stats = genie.get_stats('reliable_test')
    flaky_stats = genie.get_stats('flaky_test')
    
    print(f"\nReliability Analysis:")
    print(f"  Reliable Test: {reliable_stats.success_rate:.1f}% success rate")
    print(f"  Flaky Test:    {flaky_stats.success_rate:.1f}% success rate")


# ============================================================================
# Example 4: Using Config Overrides
# ============================================================================

def example_config_overrides():
    """Demonstrate config file and programmatic overrides"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Configuration Overrides")
    print("="*80)
    
    genie = TestingGenie('config.ini')
    
    # Register test
    genie.register_test('variable_test', test_variable_performance)
    
    # Run with config file setting
    print("\nRun 1: Using config.ini settings")
    genie.run_test('variable_test')
    
    # Run with programmatic override
    print("\nRun 2: Overriding with runs=3")
    genie.run_test('variable_test', runs=3)
    
    # Print summary showing all runs
    genie.print_summary('variable_test')


# ============================================================================
# Example 5: Export and Analysis
# ============================================================================

def example_export_results():
    """Export results for further analysis"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Exporting Results")
    print("="*80)
    
    genie = TestingGenie('config.ini')
    
    # Register multiple tests
    genie.register_test('data_processing', test_data_processing)
    genie.register_test('edge_cases', test_edge_cases)
    genie.register_test('dict_ops', test_dictionary_operations)
    
    # Run tests
    genie.run_all_tests()
    
    # Export to JSON
    output_file = 'example_results.json'
    genie.export_results(output_file)
    
    print(f"\n✓ Results have been exported to {output_file}")
    print("  You can now analyze this data with other tools (pandas, Excel, etc.)")


# ============================================================================
# Example 6: Mixed Success/Failure
# ============================================================================

def example_mixed_results():
    """Handle tests with both successes and failures"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Mixed Success and Failure")
    print("="*80)
    
    genie = TestingGenie('config.ini')
    
    # Register tests with different outcomes
    genie.register_test('always_pass', test_math_operations)
    genie.register_test('sometimes_fail', test_random_failure)
    genie.register_test('always_fail', test_intentional_failure)
    
    # Run tests
    genie.run_test('always_pass', runs=5)
    genie.run_test('sometimes_fail', runs=10)
    genie.run_test('always_fail', runs=5)
    
    # Show comparison
    genie.print_comparison()
    
    # Show detailed summary
    genie.print_summary()


# ============================================================================
# Example 7: Complete Workflow
# ============================================================================

def example_complete_workflow():
    """Demonstrate a complete testing workflow"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Complete Testing Workflow")
    print("="*80)
    
    # Step 1: Initialize
    print("\nStep 1: Initialize Testing Genie")
    genie = TestingGenie('config.ini')
    
    # Step 2: Register all tests
    print("Step 2: Register tests")
    test_suite = {
        'string_ops': test_string_operations,
        'list_ops': test_list_operations,
        'dict_ops': test_dictionary_operations,
        'math_ops': test_math_operations,
        'fast': test_fast_computation,
        'medium': test_medium_computation,
        'slow': test_slow_computation,
    }
    
    for name, func in test_suite.items():
        genie.register_test(name, func)
    
    # Step 3: Run all tests
    print("Step 3: Execute all tests")
    genie.run_all_tests()
    
    # Step 4: Analyze results
    print("\nStep 4: Analyze results")
    genie.print_summary()
    
    # Step 5: Compare tests
    print("\nStep 5: Compare performance")
    genie.print_comparison()
    
    # Step 6: Export data
    print("\nStep 6: Export results")
    genie.export_results('complete_workflow_results.json')
    
    print("\n✓ Complete workflow finished successfully!")


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print(" Testing Genie - Example Scenarios")
    print("="*80)
    
    # Uncomment the examples you want to run:
    
    example_basic_usage()
    # example_performance_comparison()
    # example_reliability_testing()
    # example_config_overrides()
    # example_export_results()
    # example_mixed_results()
    # example_complete_workflow()
    
    print("\n" + "="*80)
    print(" Examples completed!")
    print("="*80)
    print("\nTip: Uncomment other examples in the __main__ section to try them out!")
