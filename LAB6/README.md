*Lab 6 – Code Coverage and Branch Coverage Analysis*



*Course:Software Engineering Test Automation (SETA)*  

*Lab: 6*  

*Application: Solar Panel Sizing, Cost Estimation, and Payback Analysis*  

*Programming Language: Python*  

*Testing Framework: Pytest*  

*Coverage Tool:Coverage.py*



*---*



*1. Overview*



*This lab evaluates the reliability of a solar panel estimation application using automated testing. It demonstrates the difference between statement coverage and branch coverage by testing normal operations, boundary conditions, invalid inputs, and alternative execution paths.*



*2. Objectives*



*- Measure statement and branch coverage.*

*- Identify untested statements and conditional branches.*

*- Test valid inputs, invalid inputs, and boundary conditions.*

*- Achieve more than 90% code and branch coverage.*

*- Document the results using coverage reports and terminal screenshots.*



*3. Project Structure*

*LAB6/*

*├── README.md*

*├── solar\_panel\_estimate.py*

*├── test\_solar\_panel\_estimate.py*

*├── CodeCoverageTest\_solar\_panel\_estimate.py*

*├── BranchCoverageTest\_solar\_panel\_estimate.py*

*├── coverage\_analysis\_report.md*

*├── .gitignore*

*└── screenshots/*

&#x20;   *├── code\_coverage\_screenshot.png*

&#x20;   *└── branch\_coverage\_screenshot.png*

*```*



*4. Requirements*



*Install Python 3 and ensure that `python` and `pip` work in your terminal.*



*Install the required testing packages:*



*```bash*

*python -m pip install pytest coverage*

*```*



*Verify the installations:*



*```bash*

*python --version*

*python -m pytest --version*

*python -m coverage --version*

*```*



*5. How to Run the Project*



*Step 1: Open the project*



*Open Command Prompt and navigate to the repository root:*

*cmd*

*cd C:\\Users\\Dell\\Downloads\\LAB1\_AM818\_SE*



*Step 2: Run the application*



*Run the solar panel estimation program:*



*cmd*

*python LAB6\\solar\_panel\_estimate.py*



*If the application does not display anything, it may define functions without directly invoking them. In that case, run the test suites below to verify the implementation.*



*Step 3: Run the starter test suite*



*cmd*

*python -m pytest LAB6\\test\_solar\_panel\_estimate.py -v*





*This runs the starter tests and displays individual test results.*



*6. Code Coverage Testing*



*Run the code coverage test suite:*



*cmd*

*python -m coverage erase*

*python -m coverage run -m pytest LAB6\\CodeCoverageTest\_solar\_panel\_estimate.py -v*

*python -m coverage report -m*





*This measures statement coverage for the implementation.*



*Recorded result: 100% statement coverage.*



*7. Branch Coverage Testing*



*Run the branch coverage test suite:*



*cmd*

*python -m coverage erase*

*python -m coverage run --branch -m pytest LAB6\\BranchCoverageTest\_solar\_panel\_estimate.py -v*

*python -m coverage report -m*

*```*



*The --branch option measures whether conditional branches have been exercised.*



*Recorded result: 100% branch coverage.*



*8. Run All Tests Together*



*To run all three test files in one command:*



*```cmd*

*python -m pytest LAB6 -v*

*```*



*To measure coverage across the entire Lab 6 test suite:*



*```cmd*

*python -m coverage erase*

*python -m coverage run --branch -m pytest LAB6 -v*

*python -m coverage report -m*

*```*



*Note:The combined coverage percentage may differ from the individual test-suite results because the combined run measures the execution paths covered by all selected tests together.*



*9. Generate an HTML Coverage Report*



*To generate a detailed HTML report:*



*```cmd*

*python -m coverage html*

*```*



*Open the generated report:*



*```cmd*

*start htmlcov\\index.html*

*```*



*The report shows covered and uncovered lines and helps identify areas requiring additional tests.*



*10. Coverage Results*



*The recorded results in the coverage analysis report are:*



*| Test Suite | Statement Coverage | Branch Coverage |*

*|---|---:|---:|*

*| Code coverage test suite | 100% | 98% |*

*| Branch coverage test suite | 100% | 100% |*



*Both test suites exceed the required 90% coverage threshold according to the recorded results.*



*11. Project Files*



*| File | Description |*

*|---|---|*

*| `solar\_panel\_estimate.py` | Main application implementation |*

*| `test\_solar\_panel\_estimate.py` | Starter test suite |*

*| `CodeCoverageTest\_solar\_panel\_estimate.py` | Statement coverage tests |*

*| `BranchCoverageTest\_solar\_panel\_estimate.py` | Branch coverage tests |*

*| `coverage\_analysis\_report.md` | Detailed coverage analysis |*

*| `screenshots/` | Terminal screenshots of coverage results |*



*12. Key Learning Outcomes*



*- Statement coverage measures which executable statements have run.*

*- Branch coverage measures the execution of alternative decision outcomes.*

*- High statement coverage does not guarantee that every branch has been tested.*

*- Boundary-value and error-handling tests help identify defects.*

*- Automated coverage reports provide evidence of testing completeness.*



*13. Deliverables*



*- Solar panel estimation implementation.*

*- Statement coverage test suite.*

*- Branch coverage test suite.*

*- Starter test suite.*

*- Coverage analysis report.*

*- Terminal screenshots showing the recorded results.*



*14. Detailed Report*



*For the complete methodology, test scenarios, results, and analysis, see \[`coverage\_analysis\_report.md`](coverage\_analysis\_report.md).*

