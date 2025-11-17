"""
Testing Genie - A flexible testing framework with configurable runs and result comparison

Features:
- Configure test runs via config.ini file
- Set default runs globally or per-test
- Track detailed test results and statistics
- Compare results across multiple runs
- Generate comprehensive reports
"""

import time
import configparser
import json
import statistics
from datetime import datetime
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path
import traceback


@dataclass
class TestResult:
    """Stores the result of a single test run"""
    test_name: str
    run_number: int
    success: bool
    execution_time: float
    timestamp: str
    return_value: Any = None
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class TestStats:
    """Statistical summary of multiple test runs"""
    test_name: str
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float
    avg_execution_time: float
    min_execution_time: float
    max_execution_time: float
    std_dev_execution_time: float
    total_execution_time: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary for display"""
        return asdict(self)


class TestingGenie:
    """
    Main testing framework class that manages test execution, configuration, and results.
    
    Usage:
        genie = TestingGenie('config.ini')
        genie.register_test('my_test', my_test_function)
        genie.run_all_tests()
        genie.print_summary()
    """
    
    def __init__(self, config_file: str = 'config.ini'):
        """
        Initialize the Testing Genie framework
        
        Args:
            config_file: Path to the configuration INI file
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.tests: Dict[str, Callable] = {}
        self.results: Dict[str, List[TestResult]] = {}
        self.default_runs = 1
        
        self._load_config()
    
    def _load_config(self):
        """Load configuration from the INI file"""
        if not Path(self.config_file).exists():
            print(f"Warning: Config file '{self.config_file}' not found. Using defaults.")
            self.default_runs = 1
            return
        
        self.config.read(self.config_file)
        
        # Load default settings
        if 'DEFAULT' in self.config:
            self.default_runs = self.config['DEFAULT'].getint('runs', 1)
            print(f"Loaded default runs: {self.default_runs}")
        
        print(f"Configuration loaded from {self.config_file}")
    
    def register_test(self, test_name: str, test_func: Callable, runs: Optional[int] = None):
        """
        Register a test function to be run by the framework
        
        Args:
            test_name: Unique name for the test
            test_func: The test function to execute
            runs: Optional override for number of runs (uses config if not specified)
        """
        self.tests[test_name] = test_func
        print(f"Registered test: {test_name}")
    
    def _get_test_runs(self, test_name: str) -> int:
        """
        Get the number of runs for a specific test from config
        
        Args:
            test_name: Name of the test
            
        Returns:
            Number of runs (from config or default)
        """
        # Check if test has specific config section
        if test_name in self.config:
            return self.config[test_name].getint('runs', self.default_runs)
        
        return self.default_runs
    
    def run_test(self, test_name: str, runs: Optional[int] = None) -> List[TestResult]:
        """
        Run a specific test multiple times
        
        Args:
            test_name: Name of the test to run
            runs: Optional override for number of runs
            
        Returns:
            List of TestResult objects
        """
        if test_name not in self.tests:
            raise ValueError(f"Test '{test_name}' not registered")
        
        test_func = self.tests[test_name]
        num_runs = runs if runs is not None else self._get_test_runs(test_name)
        
        print(f"\n{'='*60}")
        print(f"Running test: {test_name} ({num_runs} run(s))")
        print(f"{'='*60}")
        
        results = []
        
        for run_num in range(1, num_runs + 1):
            print(f"  Run {run_num}/{num_runs}...", end=" ")
            
            start_time = time.perf_counter()
            success = True
            return_value = None
            error = None
            
            try:
                return_value = test_func()
                print("✓ PASSED")
            except Exception as e:
                success = False
                error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
                print(f"✗ FAILED: {e}")
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            result = TestResult(
                test_name=test_name,
                run_number=run_num,
                success=success,
                execution_time=execution_time,
                timestamp=datetime.now().isoformat(),
                return_value=return_value,
                error=error
            )
            
            results.append(result)
        
        # Store results
        if test_name not in self.results:
            self.results[test_name] = []
        self.results[test_name].extend(results)
        
        return results
    
    def run_all_tests(self):
        """Run all registered tests according to their configuration"""
        print(f"\n{'#'*60}")
        print(f"# Testing Genie - Running All Tests")
        print(f"# Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}")
        
        for test_name in self.tests.keys():
            self.run_test(test_name)
        
        print(f"\n{'#'*60}")
        print(f"# All tests completed!")
        print(f"{'#'*60}\n")
    
    def get_stats(self, test_name: str) -> Optional[TestStats]:
        """
        Calculate statistics for a specific test
        
        Args:
            test_name: Name of the test
            
        Returns:
            TestStats object or None if no results
        """
        if test_name not in self.results or not self.results[test_name]:
            return None
        
        results = self.results[test_name]
        execution_times = [r.execution_time for r in results]
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        return TestStats(
            test_name=test_name,
            total_runs=len(results),
            successful_runs=len(successful),
            failed_runs=len(failed),
            success_rate=(len(successful) / len(results)) * 100,
            avg_execution_time=statistics.mean(execution_times),
            min_execution_time=min(execution_times),
            max_execution_time=max(execution_times),
            std_dev_execution_time=statistics.stdev(execution_times) if len(execution_times) > 1 else 0.0,
            total_execution_time=sum(execution_times)
        )
    
    def compare_tests(self, test_names: Optional[List[str]] = None) -> Dict[str, TestStats]:
        """
        Compare statistics across multiple tests
        
        Args:
            test_names: List of test names to compare (compares all if None)
            
        Returns:
            Dictionary mapping test names to their statistics
        """
        if test_names is None:
            test_names = list(self.results.keys())
        
        comparison = {}
        for test_name in test_names:
            stats = self.get_stats(test_name)
            if stats:
                comparison[test_name] = stats
        
        return comparison
    
    def print_summary(self, test_name: Optional[str] = None):
        """
        Print a summary of test results
        
        Args:
            test_name: Specific test to summarize (summarizes all if None)
        """
        print(f"\n{'='*60}")
        print(f"  TEST SUMMARY REPORT")
        print(f"{'='*60}\n")
        
        if test_name:
            test_names = [test_name]
        else:
            test_names = list(self.results.keys())
        
        for name in test_names:
            stats = self.get_stats(name)
            if not stats:
                print(f"Test: {name} - No results available\n")
                continue
            
            print(f"Test: {name}")
            print(f"  Total Runs:      {stats.total_runs}")
            print(f"  Successful:      {stats.successful_runs} ({stats.success_rate:.1f}%)")
            print(f"  Failed:          {stats.failed_runs}")
            print(f"  Avg Time:        {stats.avg_execution_time:.6f}s")
            print(f"  Min Time:        {stats.min_execution_time:.6f}s")
            print(f"  Max Time:        {stats.max_execution_time:.6f}s")
            print(f"  Std Dev:         {stats.std_dev_execution_time:.6f}s")
            print(f"  Total Time:      {stats.total_execution_time:.6f}s")
            print()
    
    def print_comparison(self, test_names: Optional[List[str]] = None):
        """
        Print a comparison table of multiple tests
        
        Args:
            test_names: List of test names to compare (compares all if None)
        """
        comparison = self.compare_tests(test_names)
        
        if not comparison:
            print("No test results to compare")
            return
        
        print(f"\n{'='*80}")
        print(f"  TEST COMPARISON")
        print(f"{'='*80}\n")
        
        # Print header
        print(f"{'Test Name':<25} {'Runs':<8} {'Success':<10} {'Avg Time':<12} {'Total Time':<12}")
        print(f"{'-'*25} {'-'*8} {'-'*10} {'-'*12} {'-'*12}")
        
        # Print each test
        for test_name, stats in comparison.items():
            success_str = f"{stats.success_rate:.1f}%"
            avg_time_str = f"{stats.avg_execution_time:.6f}s"
            total_time_str = f"{stats.total_execution_time:.6f}s"
            
            print(f"{test_name:<25} {stats.total_runs:<8} {success_str:<10} {avg_time_str:<12} {total_time_str:<12}")
        
        print()
    
    def export_results(self, output_file: str = 'test_results.json'):
        """
        Export all test results to a JSON file
        
        Args:
            output_file: Path to the output JSON file
        """
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'tests': {}
        }
        
        for test_name, results in self.results.items():
            stats = self.get_stats(test_name)
            export_data['tests'][test_name] = {
                'statistics': stats.to_dict() if stats else None,
                'results': [r.to_dict() for r in results]
            }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"Results exported to {output_file}")
    
    def clear_results(self, test_name: Optional[str] = None):
        """
        Clear test results
        
        Args:
            test_name: Specific test to clear (clears all if None)
        """
        if test_name:
            if test_name in self.results:
                del self.results[test_name]
                print(f"Cleared results for test: {test_name}")
        else:
            self.results.clear()
            print("Cleared all test results")


# Example usage and test functions
def example_fast_test():
    """Example of a fast test"""
    time.sleep(0.01)
    return "Fast test completed"


def example_slow_test():
    """Example of a slower test"""
    time.sleep(0.1)
    return "Slow test completed"


def example_variable_test():
    """Example of a test with variable execution time"""
    import random
    time.sleep(random.uniform(0.01, 0.05))
    return "Variable test completed"


def example_failing_test():
    """Example of a test that sometimes fails"""
    import random
    if random.random() < 0.3:  # 30% chance of failure
        raise ValueError("Random failure occurred")
    return "Test passed"


if __name__ == "__main__":
    # Example usage
    print("Testing Genie Framework - Example Usage\n")
    
    # Initialize the framework
    genie = TestingGenie('config.ini')
    
    # Register tests
    genie.register_test('fast_test', example_fast_test)
    genie.register_test('slow_test', example_slow_test)
    genie.register_test('variable_test', example_variable_test)
    genie.register_test('failing_test', example_failing_test)
    
    # Run all tests
    genie.run_all_tests()
    
    # Print summary
    genie.print_summary()
    
    # Print comparison
    genie.print_comparison()
    
    # Export results
    genie.export_results()
