# Testing Genie Framework

A flexible Python testing framework that allows you to configure test runs, track detailed results, and compare performance across multiple test executions.

## Features

- **Configurable Test Runs**: Set the number of runs globally or per-test via `config.ini`
- **Detailed Result Tracking**: Track execution time, success/failure, return values, and errors
- **Statistical Analysis**: Automatically calculate statistics (mean, min, max, std dev)
- **Result Comparison**: Compare multiple tests side-by-side
- **JSON Export**: Export all results for further analysis
- **Easy to Use**: Simple API for registering and running tests

## Quick Start

### 1. Create a config.ini file

```ini
[DEFAULT]
# Default number of runs for all tests
runs = 5

[my_test]
# Override runs for specific test
runs = 10
```

### 2. Write your test code

```python
from testing_genie import TestingGenie

# Initialize the framework
genie = TestingGenie('config.ini')

# Define your test function
def my_test():
    # Your test code here
    result = 1 + 1
    assert result == 2
    return result

# Register the test
genie.register_test('my_test', my_test)

# Run all tests
genie.run_all_tests()

# View results
genie.print_summary()
genie.print_comparison()
```

## Configuration File Format

The `config.ini` file uses the INI format with sections for each test:

```ini
[DEFAULT]
runs = 5              # Default runs for all tests

[test_name_1]
runs = 10             # This test runs 10 times

[test_name_2]
runs = 3              # This test runs 3 times

[test_name_3]
# Uses default (5 runs) if not specified
```

## API Reference

### TestingGenie Class

#### `__init__(config_file='config.ini')`
Initialize the framework with a configuration file.

#### `register_test(test_name, test_func, runs=None)`
Register a test function to be executed.
- `test_name`: Unique identifier for the test
- `test_func`: Function to execute (should be callable)
- `runs`: Optional override for number of runs

#### `run_test(test_name, runs=None)`
Run a specific test multiple times.
- Returns: List of TestResult objects

#### `run_all_tests()`
Run all registered tests according to their configuration.

#### `get_stats(test_name)`
Get statistical summary for a specific test.
- Returns: TestStats object with mean, min, max, std dev, etc.

#### `compare_tests(test_names=None)`
Compare statistics across multiple tests.
- `test_names`: List of tests to compare (compares all if None)
- Returns: Dictionary of test name to TestStats

#### `print_summary(test_name=None)`
Print a detailed summary report.
- `test_name`: Specific test to summarize (all tests if None)

#### `print_comparison(test_names=None)`
Print a comparison table of test statistics.

#### `export_results(output_file='test_results.json')`
Export all results to a JSON file for further analysis.

#### `clear_results(test_name=None)`
Clear stored results.

## Example Usage Patterns

### Pattern 1: Basic Testing

```python
from testing_genie import TestingGenie

genie = TestingGenie('config.ini')

def simple_test():
    return sum([1, 2, 3, 4, 5])

genie.register_test('simple_test', simple_test)
genie.run_all_tests()
genie.print_summary()
```

### Pattern 2: Performance Comparison

```python
from testing_genie import TestingGenie
import time

genie = TestingGenie('config.ini')

def algorithm_v1():
    time.sleep(0.1)
    return "v1"

def algorithm_v2():
    time.sleep(0.05)
    return "v2"

genie.register_test('algo_v1', algorithm_v1)
genie.register_test('algo_v2', algorithm_v2)
genie.run_all_tests()
genie.print_comparison()
```

### Pattern 3: Reliability Testing

```python
from testing_genie import TestingGenie
import random

genie = TestingGenie('config.ini')

def flaky_test():
    if random.random() < 0.1:  # 10% failure rate
        raise Exception("Random failure")
    return "success"

genie.register_test('flaky_test', flaky_test)
genie.run_test('flaky_test', runs=100)  # Run 100 times
stats = genie.get_stats('flaky_test')
print(f"Success rate: {stats.success_rate}%")
```

### Pattern 4: Export and Analyze

```python
from testing_genie import TestingGenie

genie = TestingGenie('config.ini')

# ... register and run tests ...

# Export results
genie.export_results('my_results.json')

# Results can be loaded and analyzed with other tools
import json
with open('my_results.json', 'r') as f:
    data = json.load(f)
    # Analyze with pandas, plot with matplotlib, etc.
```

## Output Examples

### Summary Report
```
==============================================================
  TEST SUMMARY REPORT
==============================================================

Test: fast_test
  Total Runs:      10
  Successful:      10 (100.0%)
  Failed:          0
  Avg Time:        0.010234s
  Min Time:        0.010001s
  Max Time:        0.010500s
  Std Dev:         0.000156s
  Total Time:      0.102340s
```

### Comparison Table
```
================================================================================
  TEST COMPARISON
================================================================================

Test Name                 Runs     Success    Avg Time     Total Time  
------------------------- -------- ---------- ------------ ------------
fast_test                 10       100.0%     0.010234s    0.102340s   
slow_test                 3        100.0%     0.100123s    0.300369s   
```

## Advanced Features

### Custom Test Functions
Test functions can:
- Accept no parameters
- Return any value (captured in results)
- Raise exceptions (captured as failures)
- Use external libraries and dependencies

### Result Data Structure
Each test run captures:
- Test name and run number
- Success/failure status
- Execution time (high precision)
- Timestamp (ISO format)
- Return value
- Error details (if failed)

### Statistics Calculated
- Total runs, successful runs, failed runs
- Success rate (percentage)
- Average execution time
- Min/max execution time
- Standard deviation
- Total execution time

## Best Practices

1. **Use descriptive test names**: Makes results easier to interpret
2. **Set appropriate run counts**: More runs = better statistics, but longer execution
3. **Export results regularly**: Keep historical data for trend analysis
4. **Compare similar tests**: Group related tests for meaningful comparisons
5. **Handle exceptions properly**: Let the framework catch them for accurate failure tracking

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details
