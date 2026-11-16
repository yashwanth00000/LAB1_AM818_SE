# LAB 7 — Fuzzing for Input Validation Bugs

**Student:** Yashwanth Gowda T G  
**SRN:** PES1UG25AM818

This folder contains the fixed solar-panel estimate parser, Hypothesis property-based tests, and report for Lab 7. See `LAB7_REPORT.md` for the methodology, findings, fixes, and reflection answers.

Install and run from this directory:

```bash
python -m pip install -r requirements.txt
python solar_panel_estimate_parser.py
python -m pytest -q test_solar_panel_estimate_parser.py
```

Add four genuine terminal screenshots to `evidence/`: `SS1_buggy_run.png`, `SS2_failing_tests.png`, `SS3_fixed_run.png`, and `SS4_passing_tests.png`. Capture SS1 and SS2 against the original buggy source before replacing it. No screenshots are fabricated.