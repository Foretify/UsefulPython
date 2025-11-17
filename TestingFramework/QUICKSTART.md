# Testing Genie - Quick Start Guide

Get started with Testing Genie in 5 minutes!

## Step 1: Create config.ini

Create a `config.ini` file in your project directory:

```ini
[DEFAULT]
runs = 5

[my_first_test]
runs = 10
```

## Step 2: Write Your Test Script

Create a Python file (e.g., `my_tests.py`):

```python
from testing_genie import TestingGenie

# Initialize
genie = TestingGenie('config.ini')

# Define a test function
def my_first_test():
    result = 2 + 2
    assert result == 4, "Math is broken!"
    return result

# Register and run
genie.register_test('my_first_test', my_first_test)
genie.run_all_tests()

# View results
genie.print_summary()
```

## Step 3: Run Your Tests

```bash
python my_tests.py
```

## That's it!

You now have:
- ✓ Configurable test runs
- ✓ Automatic statistics
- ✓ Detailed result tracking
- ✓ Performance analysis

## Next Steps

### Add More Tests

```python
def test_two():
    return "Hello" + " " + "World"

def test_three():
    data = [1, 2, 3]
    return sum(data)

genie.register_test('test_two', test_two)
genie.register_test('test_three', test_three)
```

### Compare Performance

```python
genie.run_all_tests()
genie.print_comparison()  # See side-by-side comparison
```

### Export Results

```python
genie.export_results('my_results.json')
```

### Override Runs Programmatically

```python
# Run specific test with custom run count
genie.run_test('my_first_test', runs=50)
```

## Configuration Options

The `config.ini` file supports:

```ini
[DEFAULT]
runs = 5              # Default for all tests

[specific_test]
runs = 20             # Override for this test only

[another_test]
# No runs specified = uses DEFAULT
```

## Common Patterns

### Pattern 1: Performance Testing
```python
def fast_algorithm():
    return sum(range(100))

def slow_algorithm():
    total = 0
    for i in range(100):
        total += i
    return total

genie.register_test('fast', fast_algorithm)
genie.register_test('slow', slow_algorithm)
genie.run_all_tests()
genie.print_comparison()
```

### Pattern 2: Reliability Testing
```python
import random

def flaky_function():
    if random.random() < 0.1:  # 10% failure
        raise Exception("Oops!")
    return "OK"

genie.register_test('flaky', flaky_function)
genie.run_test('flaky', runs=100)
stats = genie.get_stats('flaky')
print(f"Success rate: {stats.success_rate}%")
```

### Pattern 3: Statistical Analysis
```python
genie.run_all_tests()

for test_name in genie.tests.keys():
    stats = genie.get_stats(test_name)
    print(f"{test_name}:")
    print(f"  Mean: {stats.avg_execution_time:.6f}s")
    print(f"  Std Dev: {stats.std_dev_execution_time:.6f}s")
```

## Tips

1. **Use descriptive test names** - easier to identify in reports
2. **Set runs based on test duration** - fast tests can run more times
3. **Export results regularly** - build historical data
4. **Let tests raise exceptions** - framework captures them automatically
5. **Return meaningful values** - they're captured in results

## Full Example

```python
from testing_genie import TestingGenie
import time

# Initialize
genie = TestingGenie('config.ini')

# Define tests
def test_addition():
    assert 1 + 1 == 2
    return "passed"

def test_performance():
    time.sleep(0.01)
    return "completed"

# Register
genie.register_test('addition', test_addition)
genie.register_test('performance', test_performance)

# Run
genie.run_all_tests()

# Analyze
genie.print_summary()
genie.print_comparison()
genie.export_results('results.json')

print("Testing complete!")
```

## Need Help?

- Check `README.md` for full documentation
- See `examples.py` for more scenarios
- Review `testing_genie.py` for API details

## Advanced Usage

For more advanced features, see:
- `README.md` - Complete API reference
- `examples.py` - 7 detailed examples
- `testing_genie.py` - Source code with docstrings

Happy Testing! 🧞‍♂️
