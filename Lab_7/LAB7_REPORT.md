# LAB 7 Report — Fuzzing for Input Validation Bugs

**Name:** Yashwanth Gowda T G  
**SRN:** PES1UG25AM818

## 1. Objective

Apply Hypothesis property-based fuzzing to identify edge-case failures in the three solar estimate parsing functions, correct the input validation, and verify robust behaviour.

## 2. Functions tested

- clean_site_name(name): trims and normalizes a site name while removing # and @.
- parse_monthly_units(text): converts a whole-number monthly electricity reading, optionally followed by kWh, to an integer.
- panels_for_roof(text): parses two positive roof dimensions and calculates the number of 18-square-foot panels that fit.

## 3. Fuzzing method

The tests use @given with Hypothesis strategies. Inputs include arbitrary Unicode text, None, integers, floating-point values (including NaN and infinity), booleans, and lists. Each parser is checked for a stable return type and a non-negative numeric result where applicable. Additional properties verify marker removal, valid unit conversion, and the roof-area calculation.

Install and run:

    python -m pip install hypothesis pytest
    python -m pytest -q test_solar_panel_estimate_parser.py

## 4. Bugs and hardening changes

| Function | Original weakness | Defensive change |
|---|---|---|
| clean_site_name | Calling strip() on None or a non-string raises; control characters and irregular whitespace are not normalized | Safely return an empty string for non-strings; remove non-printable characters and markers; collapse whitespace |
| parse_monthly_units | Calling lower() on non-strings fails; malformed numbers can raise ValueError | Validate non-negative whole number with optional trailing kWh; invalid inputs return 0 |
| panels_for_roof | Missing dimensions, extra separators, malformed numbers, or non-string values can raise | Validate complete dimension format; accept x, X, or × and optional ft; require positive dimensions; invalid inputs return 0 |

## 5. Reflection questions and answers

### Q1. What is fuzz testing, and why is it useful?

Fuzz testing is a dynamic testing technique that supplies random, unexpected, or malformed inputs to a program. It is useful because manually written test cases may miss unusual edge cases. A fuzzer can discover crashes, incorrect behaviour, and weaknesses in input validation that were not anticipated by the developer.

### Q2. How does Hypothesis help find bugs?

Hypothesis is a property-based testing library. The developer describes expected properties and input strategies using @given. Hypothesis automatically generates many inputs, reports inputs that violate a property, and minimizes failures to a simpler example that is easier to debug and reproduce.

### Q3. How did you improve the robustness of the application?

I added type checks and strict input-format validation, handled malformed values without unhandled exceptions, restricted numeric values to supported ranges, and used safe documented fallback results. I then used property-based tests to check the functions against a broad range of generated inputs.

## 6. Evidence

Add four genuine execution screenshots to the screenshot folder and final PDF:

- SS1 — original buggy script execution.
- SS2 — failing Hypothesis tests against the original buggy script.
- SS3 — fixed script execution.
- SS4 — passing Hypothesis tests against the fixed script.

Capture the initial buggy outputs before replacing the starter source files, then capture the fixed outputs after applying the fixes. No screenshots are fabricated.

## 7. Conclusion

Hypothesis fuzzing exposes assumptions that ordinary examples do not exercise. Explicit type and format validation makes these parsers more robust, and property-based tests provide repeatable checks against edge cases.
