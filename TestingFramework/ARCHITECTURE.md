# Testing Genie - Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TESTING GENIE FRAMEWORK                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: CONFIGURATION                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   config.ini                                                        │
│   ┌──────────────────────────┐                                     │
│   │ [DEFAULT]                │                                     │
│   │ runs = 5                 │─────┐                               │
│   │                          │     │                               │
│   │ [test_1]                 │     │  Loaded by                    │
│   │ runs = 10                │     │  TestingGenie.__init__()      │
│   │                          │     │                               │
│   │ [test_2]                 │     │                               │
│   │ runs = 3                 │─────┘                               │
│   └──────────────────────────┘                                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: TEST REGISTRATION                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   genie = TestingGenie('config.ini')                               │
│                                                                      │
│   genie.register_test('test_1', test_func_1)                       │
│   genie.register_test('test_2', test_func_2)                       │
│                                                                      │
│   ┌─────────────────────────────────────────┐                      │
│   │  self.tests = {                         │                      │
│   │    'test_1': test_func_1,               │                      │
│   │    'test_2': test_func_2                │                      │
│   │  }                                      │                      │
│   └─────────────────────────────────────────┘                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: TEST EXECUTION                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   genie.run_all_tests()                                            │
│          │                                                          │
│          ├──► For each test:                                       │
│          │    1. Read run count from config                        │
│          │    2. Execute N times                                   │
│          │    3. Track results                                     │
│          │                                                          │
│          └──► Flow:                                                │
│                                                                      │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐   │
│   │   Run #1     │─────►│   Run #2     │─────►│   Run #N     │   │
│   └──────────────┘      └──────────────┘      └──────────────┘   │
│         │                      │                      │            │
│         ▼                      ▼                      ▼            │
│   ┌──────────────────────────────────────────────────────┐        │
│   │  Capture for each run:                              │        │
│   │  • Success/Failure                                  │        │
│   │  • Execution Time (high precision)                  │        │
│   │  • Return Value                                     │        │
│   │  • Error/Exception (if any)                         │        │
│   │  • Timestamp                                        │        │
│   └──────────────────────────────────────────────────────┘        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: RESULT STORAGE                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   self.results = {                                                 │
│     'test_1': [                                                    │
│       TestResult(run=1, success=True, time=0.123, ...),           │
│       TestResult(run=2, success=True, time=0.125, ...),           │
│       TestResult(run=3, success=False, time=0.121, ...),          │
│       ...                                                          │
│     ],                                                             │
│     'test_2': [                                                    │
│       TestResult(run=1, success=True, time=0.456, ...),           │
│       ...                                                          │
│     ]                                                              │
│   }                                                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 5: STATISTICAL ANALYSIS                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   genie.get_stats('test_1')                                        │
│          │                                                          │
│          └──► Calculate:                                           │
│                                                                      │
│   ┌────────────────────────────────────────────────────┐           │
│   │  TestStats:                                        │           │
│   │  • total_runs = 10                                 │           │
│   │  • successful_runs = 9                             │           │
│   │  • failed_runs = 1                                 │           │
│   │  • success_rate = 90.0%                            │           │
│   │  • avg_execution_time = 0.124s                     │           │
│   │  • min_execution_time = 0.121s                     │           │
│   │  • max_execution_time = 0.127s                     │           │
│   │  • std_dev_execution_time = 0.002s                 │           │
│   │  • total_execution_time = 1.24s                    │           │
│   └────────────────────────────────────────────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 6: OUTPUT & COMPARISON                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Three output formats:                                            │
│                                                                      │
│   1. DETAILED SUMMARY                                              │
│      genie.print_summary()                                         │
│      └──► Per-test detailed statistics                            │
│                                                                      │
│   2. COMPARISON TABLE                                              │
│      genie.print_comparison()                                      │
│      └──► Side-by-side comparison of all tests                    │
│                                                                      │
│   3. JSON EXPORT                                                   │
│      genie.export_results('output.json')                          │
│      └──► Full data export for external analysis                  │
│                                                                      │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐│
│   │   Console       │   │  Comparison     │   │  JSON File      ││
│   │   Summary       │   │  Table          │   │  Export         ││
│   └─────────────────┘   └─────────────────┘   └─────────────────┘│
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  DATA STRUCTURES                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   TestResult (per run)          TestStats (per test)               │
│   ┌────────────────────┐        ┌────────────────────┐            │
│   │ • test_name        │        │ • test_name        │            │
│   │ • run_number       │        │ • total_runs       │            │
│   │ • success          │        │ • successful_runs  │            │
│   │ • execution_time   │        │ • failed_runs      │            │
│   │ • timestamp        │        │ • success_rate     │            │
│   │ • return_value     │        │ • avg_time         │            │
│   │ • error            │        │ • min_time         │            │
│   └────────────────────┘        │ • max_time         │            │
│                                  │ • std_dev          │            │
│                                  │ • total_time       │            │
│                                  └────────────────────┘            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  WORKFLOW SUMMARY                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   1. Load config.ini                                               │
│          ▼                                                          │
│   2. Register test functions                                       │
│          ▼                                                          │
│   3. Execute tests (N runs each)                                   │
│          ▼                                                          │
│   4. Store results (TestResult objects)                            │
│          ▼                                                          │
│   5. Calculate statistics (TestStats)                              │
│          ▼                                                          │
│   6. Output results (console/JSON)                                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  KEY FEATURES                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ✓ Config-driven test runs (INI format)                           │
│  ✓ Per-test and global configuration                               │
│  ✓ Detailed result tracking                                        │
│  ✓ Statistical analysis (mean, std dev, etc.)                      │
│  ✓ Result comparison across tests                                  │
│  ✓ JSON export for further analysis                                │
│  ✓ Error capture and reporting                                     │
│  ✓ High-precision timing                                           │
│  ✓ Return value capture                                            │
│  ✓ Success/failure rate tracking                                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
