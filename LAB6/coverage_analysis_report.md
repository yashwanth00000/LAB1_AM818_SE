# Lab 6: Code and Branch Coverage Analysis Report

**Course / Lab:** Software Engineering Test Automation (SETA) — Lab 6  
**Module Under Test:** `solar_panel_estimate.py`  
**Application Domain:** Solar Panel Sizing, Cost Estimation, and Payback Analysis  

---

## 1. Objectives & Overview

The objective of this lab is to:
1. Differentiate clearly between **Line (Statement) Coverage** and **Branch Coverage**.
2. Measure and analyze code execution paths using Python's `coverage` tool and `pytest`.
3. Demonstrate that high/100% line coverage can leave critical logical branches untested.
4. Design comprehensive test suites addressing all edge cases, decision branches, and boundary conditions to achieve **100% Code Coverage** and **100% Branch Coverage** (well exceeding the >90% requirement).

---

## 2. Theoretical Concepts

| Coverage Type | Definition | Key Metric / Question |
| :--- | :--- | :--- |
| **Line (Statement) Coverage** | Measures the percentage of executable source code statements evaluated at least once during test execution. | *Did the execution pass through this line of code?* |
| **Branch Coverage** | Measures whether every decision point / control flow branch (`if`, `elif`, `else`, ternary, compound conditions) evaluated to both `True` and `False`. | *Did every conditional decision follow both True and False pathways?* |

> **Key Takeaway:** Line coverage can give a false sense of security. A suite may execute 100% of the lines in a function by taking only one conditional path (e.g., only `True`), while the alternative path (e.g., `False`) remains completely unverified. Branch coverage forces testing of all alternate logical pathways and edge cases.

---

## 3. Initial Baseline Analysis (Starter Tests)

The repository originally contained two basic test cases in `test_solar_panel_estimate.py`:
- `test_mono_exact()`
- `test_concrete_roof()`

### Initial Execution Results:

```bash
coverage run -m pytest test_solar_panel_estimate.py
coverage report -m
```

```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
solar_panel_estimate.py           40     20    50%   6, 8, 13, 15, 21, 24, 26, 28, 30, 32, 37-46
test_solar_panel_estimate.py       6      0   100%
------------------------------------------------------------
TOTAL                             46     20    57%
```

### Initial Branch Coverage Results:

```bash
coverage run --branch -m pytest test_solar_panel_estimate.py
coverage report -m
```

```
Name                           Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------
solar_panel_estimate.py           40     20     26     10    45%   6, 8, 13, 15, 21, 24, 26, 28, 30, 32, 37-46
test_solar_panel_estimate.py       6      0      0      0   100%
--------------------------------------------------------------------------
TOTAL                             46     20     26     10    50%
```

**Observation:**
- **Line Coverage:** 50% (20 missed lines out of 40 statements).
- **Branch Coverage:** 45% (10 partial branches, multiple decisions unexecuted).
- The entire `payback_years` function and error-handling branches in `panels_needed` and `install_cost` were unexecuted.

---

## 4. Code Coverage Analysis & Improvement (>90% Target)

### Target File: `CodeCoverageTest_solar_panel_estimate.py`

Test cases were designed to ensure that every statement in `solar_panel_estimate.py` was executed at least once:
- `test_panels_needed_unknown_panel_type`: Executes `raise ValueError("unknown panel type")` (lines 5-6).
- `test_panels_needed_invalid_monthly_units`: Executes `raise ValueError("invalid input")` (lines 7-8).
- `test_panels_needed_with_remainder`: Executes `panels += 1` on remainder (lines 9-13).
- `test_panels_needed_minimum_panel_clamp`: Executes `panels = 2` minimum clamp (lines 14-16).
- `test_install_cost_invalid_panels`: Executes `raise ValueError("invalid panel count")` (lines 20-21).
- `test_install_cost_tin_roof`: Executes `cost += 8000` (lines 23-24).
- `test_install_cost_tiled_roof`: Executes `cost += panels * 2000` (lines 25-26).
- `test_install_cost_unknown_roof`: Executes `raise ValueError("unknown roof type")` (lines 27-28).
- `test_install_cost_concrete_with_battery`: Executes `cost += 60000` (line 30).
- `test_install_cost_bulk_discount`: Executes `cost -= cost // 10` (lines 31-33).
- `test_payback_years_non_positive_saving`: Executes `return -1` (lines 37-38).
- `test_payback_years_high_subsidy_capped`: Executes `subsidy_percent = 40` (lines 39-40).
- `test_payback_years_with_remainder`: Executes `years += 1` on remainder (lines 41-46).

### Execution Command:
```bash
coverage run -m pytest CodeCoverageTest_solar_panel_estimate.py
coverage report -m
```

### Result:
```
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
CodeCoverageTest_solar_panel_estimate.py      32      0   100%
solar_panel_estimate.py                       40      0   100%
------------------------------------------------------------------------
TOTAL                                         72      0   100%
```

**Outcome:** Achieved **100% Statement / Line Coverage** (40/40 statements, 0 missing).

---

## 5. Why Line Coverage != Branch Coverage (Gap Analysis)

When running the branch coverage report against `CodeCoverageTest_solar_panel_estimate.py`:

```bash
coverage run --branch -m pytest CodeCoverageTest_solar_panel_estimate.py
coverage report -m
```

```
Name                                       Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------------------
CodeCoverageTest_solar_panel_estimate.py      32      0      0      0   100%
solar_panel_estimate.py                       40      0     26      1    98%   12->14
--------------------------------------------------------------------------------------
TOTAL                                         72      0     26      1    99%
```

**Missing Branch Detected:**
- Branch `12->14`: In `if daily_wh % per_panel_wh:`, the test suite only provided an input with a remainder (`True` branch to execute line 13 `panels += 1`). The exact division path (`False` branch where remainder is 0) was never exercised!
- Similarly, compound condition `sun_hours <= 0` and alternate roof / subsidy boundary combinations were not thoroughly tested.

---

## 6. Branch Coverage Analysis & Improvement (>90% Target)

### Target File: `BranchCoverageTest_solar_panel_estimate.py`

To achieve **100% Branch Coverage**, 26 targeted tests were implemented to cover both `True` and `False` outcomes for every control branch, edge cases, and boundary values:

1. **`panels_needed` Branches:**
   - Unsupported panel type (`True` -> `ValueError`)
   - `monthly_units <= 0` (`0` and negative values)
   - `sun_hours <= 0` (`0` and negative values)
   - Remainder != 0 (`True` -> `panels += 1`)
   - Remainder == 0 (`False` -> branch `12->14` covered)
   - Both panel types in dictionary: `mono` (400W) and `poly` (330W)
   - Minimum clamp: `panels < 2` (`True` -> 2, `False` -> retains >= 2)

2. **`install_cost` Branches:**
   - `panels < 1` (`0` and negative values)
   - Roof types: `tin`, `tiled`, `concrete`, and unknown (e.g. `slate`)
   - Battery: `has_battery = True` and `has_battery = False`
   - Discount threshold: exactly `10` panels (`True`), `12` panels (`True`), and `9` panels (`False`)

3. **`payback_years` Branches:**
   - `monthly_saving <= 0` (`0` and `-500`)
   - `subsidy_percent > 40` (`60%` capped to `40%`)
   - Boundary: `subsidy_percent == 40` and `subsidy_percent = 20`
   - Exact division: `net_cost % yearly_saving == 0` (`False` branch)
   - Non-exact division: `net_cost % yearly_saving != 0` (`True` branch -> `years += 1`)

### Execution Command:
```bash
coverage run --branch -m pytest BranchCoverageTest_solar_panel_estimate.py
coverage report -m
```

### Result:
```
Name                                         Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------------------
BranchCoverageTest_solar_panel_estimate.py      62      0      0      0   100%
solar_panel_estimate.py                         40      0     26      0   100%
----------------------------------------------------------------------------------------
TOTAL                                          102      0     26      0   100%
```

**Outcome:** Achieved **100% Branch Coverage** (26/26 branches, 0 missing branches).

---

## 7. Deliverables Summary Checklist

| Deliverable | Required By Handout | Status | File / Artifact |
| :--- | :--- | :--- | :--- |
| **Code Coverage Test Suite** | `CodeCoverageTest_xxxx_application.py` | Complete (100% Line Cov) | `LAB6/CodeCoverageTest_solar_panel_estimate.py` |
| **Branch Coverage Test Suite** | `BranchCoverageTest_xxxx_application.py` | Complete (100% Branch Cov) | `LAB6/BranchCoverageTest_solar_panel_estimate.py` |
| **Full Starter Test Suite** | Updated `test_solar_panel_estimate.py` | Complete (100% Line & Branch) | `LAB6/test_solar_panel_estimate.py` |
| **Code Coverage Screenshot** | Terminal Output Screenshot | Generated | `LAB6/code_coverage.png` & `LAB6/screenshots/code_coverage_analysis.png` |
| **Branch Coverage Screenshot**| Terminal Output Screenshot | Generated | `LAB6/branch_coverage.png` & `LAB6/screenshots/branch_coverage_analysis.png` |
| **Minimum 2 Git Commits** | Commit 1: Code Cov; Commit 2: Branch Cov | Complete | Documented in Git history |
| **Comprehensive Report** | Lab 6 Report & Analysis | Complete | `LAB6/coverage_analysis_report.md` |

---

## 8. Verification Commands

To reproduce the results at any time:

```bash
# 1. Run Code Coverage
coverage run -m pytest LAB6/CodeCoverageTest_solar_panel_estimate.py
coverage report -m

# 2. Run Branch Coverage
coverage run --branch -m pytest LAB6/BranchCoverageTest_solar_panel_estimate.py
coverage report -m

# 3. Run full test suite with branch coverage
coverage run --branch -m pytest LAB6/test_solar_panel_estimate.py
coverage report -m
```
