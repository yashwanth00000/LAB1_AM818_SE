# Lab 5: Static Code Analysis — Comprehensive Lab Report

**Course:** Version Control & Software Engineering Lab (VCS)  
**Topic:** Static Code Analysis using Pylint, Bandit, and Flake8  
**Assigned Repository:** `L5_65_auction-bidding-main`  
**Primary Script:** `auction_system.py`  

---

## 1. Executive Summary

This laboratory exercise focused on conducting rigorous static code analysis and security auditing on an online auction and bidding system (`auction_system.py`). Using industry-standard tools (**Pylint**, **Bandit**, and **Flake8**), multiple vulnerabilities, code quality smells, style violations, and subtle business logic bugs were detected, documented, and remediated.

Through an iterative refactoring methodology across three dedicated Git commits, the codebase was elevated from an error-prone, insecure baseline (Pylint score: **6.09/10**, **3 Bandit vulnerabilities**, **19 Flake8 errors**) to an industry-standard, fully compliant release achieving:
- **Pylint Score:** **10.00 / 10.00** (+3.91 improvement)
- **Bandit Vulnerabilities:** **0** (All High and Medium severity issues mitigated)
- **Flake8 Violations:** **0** (100% PEP 8 compliant)
- **Functional Integrity:** Fixed date comparison bug, prohibited shill bidding, and enforced reserve prices and minimum increments.

---

## 2. Tools & Analysis Metrics Summary

| Static Analysis Tool | Focus Area | Before Refactoring | After Refactoring | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Bandit** | Application Security & Vulnerability Detection | 3 Issues (2 High, 1 Medium) | **0 Issues** | **PASS** |
| **Pylint** | Code Quality, Design, Docstrings & Conventions | 6.09 / 10.00 | **10.00 / 10.00** | **PASS** |
| **Flake8** | PEP 8 Formatting, Whitespace & Line Length | 19 Violations (E302, E305, E501) | **0 Violations** | **PASS** |

---

## 3. Detailed Issue Identification & Remediation Log

| # | Issue ID / Name | Tool | Severity | Location | Root Cause | Implemented Resolution |
| :-: | :--- | :---: | :---: | :--- | :--- | :--- |
| **1** | `B411:blacklist` | Bandit | High | Line 5 | Using standard `xmlrpc.client` is susceptible to XML entity expansion and XXE attacks. | Applied `defusedxml.xmlrpc.monkey_patch()` and marked safe with `# nosec B411`. |
| **2** | `B701:jinja2_autoescape` | Bandit | High | Line 65 | `Environment(autoescape=False)` disables HTML escaping, allowing XSS via auction titles. | Configured `Environment(autoescape=True)` to auto-escape all dynamic template variables. |
| **3** | `B704:markupsafe_xss` | Bandit | Medium | Line 70 | Unescaped string concatenation passed into `Markup(...)` permitted HTML/JS injection. | Sanitized dynamic input with `markupsafe.escape(name)` before `Markup` formatting. |
| **4** | Date Lexicographical Bug | Logic | High | Line 22 | Comparing timestamps as raw strings caused morning bids (`"9:30"`) to sort as after close (`"18:00"`). | Parsed strings into `datetime` objects with `datetime.strptime` for true chronological comparison. |
| **5** | Self-Bidding / Shill Bug | Logic | High | Line 24 | Sellers could place bids on their own items (`seller_sam`), artificially inflating lot prices. | Added guard condition `if bidder == self.seller: return False`. |
| **6** | Reserve Price Ignored | Logic | High | Line 32, 38 | `reserve_price` was never verified, allowing items to be won below reserve or with Rs. 0 bids. | Updated `winner()` and `final_price()` to verify `self.highest >= self.reserve_price`. |
| **7** | Minimum Increment Bug | Logic | Medium | Line 24 | `amount >= self.highest` accepted bids with zero or insufficient increment (< `MIN_INCREMENT`). | Required `amount >= self.highest + MIN_INCREMENT` for subsequent bids and positive initial bids. |
| **8** | `W0719` / `W0718` Broad Exceptions | Pylint | Medium | Line 23, 50 | Raising and catching generic `Exception` obscured specific failure modes and masked errors. | Created custom `AuctionError` and `AuctionClosedError`; caught explicit exceptions only. |
| **9** | `W0201` / `R0902` Attribute Smell | Pylint | Medium | Line 27 | `self.leader` defined outside `__init__`; class exceeded 7 instance attributes. | Refactored `leader` into a clean `@property` dynamically referencing `self.bids[-1][0]`. |
| **10** | `R0205` Redundant Inheritance | Pylint | Low | Line 11 | `class Auction(object)` inherits from `object`, redundant in Python 3. | Cleaned definition to `class Auction:`. |
| **11** | `R1705` / `R1724` Redundant Else | Pylint | Low | Line 29, 60 | Unnecessary `else` blocks after `return` and `continue` increased indentation depth. | Removed redundant `else` branches and de-indented sequential logic. |
| **12** | `C0114`–`C0116` Missing Docs | Pylint | Low | Multi | Missing docstrings across modules, classes, and all functions. | Added PEP 257 compliant docstrings describing purpose, arguments, and return values. |
| **13** | `C0103` Naming Style | Pylint | Low | Multi | Functions and methods used `camelCase` naming instead of PEP 8 `snake_case`. | Renamed to `snake_case` with backward-compatible aliases for complete API compatibility. |
| **14** | `E302` / `E305` Blank Lines | Flake8 | Low | Multi | Top-level functions and classes lacked standard 2 blank lines separation. | Inserted standard 2 blank lines before and after all classes and top-level functions. |
| **15** | `E501` Line Length | Flake8 | Low | Multi | Statements and long strings exceeded PEP 8 limit of 79 characters. | Wrapped lines and formatted multi-line arguments to adhere to the 79-character limit. |

---

## 4. Execution Output Comparison

### Original Output (Buggy & Vulnerable)
```text
Asha bids 3000: True
Ben bids 3000 (same amount): True           <-- Bug: Accepted identical bid
Asha bids 3050 (+50): True                  <-- Bug: Ignored MIN_INCREMENT (100)
Seller bids on own item: True               <-- Bug: Shill bidding permitted
Bid at 9:30 AM (before 18:00 close): False  <-- Bug: String comparison rejected valid bid
Late bid (next day): False
Winner: seller_sam                          <-- Bug: Seller won own auction below reserve
Final price (reserve 5000): 4200.0          <-- Bug: Sold below reserve price 5000
Top bidders: ['seller_sam', 'asha', 'ben']
Rs.0 bid on LOT3 (reserve 800): True        <-- Bug: Rs. 0 bid accepted
LOT3 winner: carl                           <-- Bug: Carl won with Rs. 0 on reserve 800
No-bid winner: None
Listing HTML: <h2><script>alert('pwned')</script>Old Radio</h2><p>Current bid: Rs.0</p> <-- Vulnerability: Raw XSS!
Badge: <span class='bidder'><img src=x onerror=alert(1)></span>                         <-- Vulnerability: Raw XSS!
```

### Refactored Output (Secure & Correct)
```text
Asha bids 3000: True
Ben bids 3000 (same amount): False          <-- Fixed: Rejected (must exceed highest + MIN_INCREMENT)
Asha bids 3050 (+50): False                 <-- Fixed: Rejected (increment must be >= 100)
Seller bids on own item: False              <-- Fixed: Prohibited shill bidding
Bid at 9:30 AM (before 18:00 close): True   <-- Fixed: Correctly parsed datetime; accepted on-time bid
Late bid (next day): False
Winner: None                                <-- Fixed: Dev's 4500 < reserve 5000; no winner declared
Final price (reserve 5000): 0.0             <-- Fixed: Unsold lot returns 0.0 final price
Top bidders: ['dev', 'asha']                <-- Fixed: Accurate list of legitimate bidders
Rs.0 bid on LOT3 (reserve 800): False       <-- Fixed: Non-positive bids rejected
LOT3 winner: None                           <-- Fixed: No winner when bids are missing/invalid
No-bid winner: None
Listing HTML: <h2>&lt;script&gt;alert(&#39;pwned&#39;)&lt;/script&gt;Old Radio</h2><p>Current bid: Rs.0</p> <-- Fixed: Escaped!
Badge: <span class='bidder'>&lt;img src=x onerror=alert(1)&gt;</span>                         <-- Fixed: Escaped!
```

---

## 5. Git Commit Log (Deliverable Verification)

Three structured commits were executed to cleanly isolate each tool's remediation scope:

```bash
* 258823d Refactor code quality, exception handling, logic bugs, and docstrings for Pylint 10/10
* 173bdeb Resolve PEP 8 style, line length, and formatting issues reported by Flake8
* 8300302 Fix security vulnerabilities reported by Bandit (B411, B701, B704)
* ee47a31 Initial commit: baseline auction system code and before reports
```

1. **Commit 1 (`8300302`):** Security fixes resolving all Bandit findings (B411, B701, B704).
2. **Commit 2 (`173bdeb`):** Style, indentation, whitespace, and line-length formatting resolving all Flake8 findings.
3. **Commit 3 (`258823d`):** Semantic refactoring, custom exceptions, property abstraction, logic bug fixes, docstrings, and Pylint 10.00/10 score.

---

## 6. Deliverables Checklist

- [x] **3 Git Commits:** Cleanly tracking changes for Bandit, Flake8, and Pylint.
- [x] **pylint_report.txt / pylint_report_before.txt / pylint_report_after.txt:** Validating baseline 6.09/10 and final 10.00/10.
- [x] **bandit_report.txt / bandit_report_before.txt / bandit_report_after.txt:** Validating baseline 3 issues and final 0 issues.
- [x] **flake8_report.txt / flake8_report_before.txt / flake8_report_after.txt:** Validating baseline 19 issues and final 0 issues.
- [x] **Updated Python Source File (`auction_system.py`):** Fully operational, secure, and robust.
- [x] **Issue Log Table (`issues.md`):** Complete table with issue types, lines, descriptions, and fixes.
- [x] **Reflection Questions (`reflection.md`):** Comprehensive answers covering learning outcomes.
- [x] **Comprehensive Lab Report (`report.md`):** Detailed analysis, metrics, and documentation.
