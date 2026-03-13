# Documentation assets

Sample screenshots and terminal outputs from test and automation runs. Referenced from the main README.

| File | Description |
|------|-------------|
| `all-tests-output.png` | Terminal output for full suite (16 tests) |
| `regression-tests-output.png` | Terminal output for regression tests (12 tests) |
| `smoke-tests-output.png` | Terminal output for smoke tests (4 tests) |
| `html-tests-output.png` | Example of HTML report generation |
| `myntra-automation-output.png` | Output from standalone automation run (open_myntra_home.py) |
| `failure-test-output.png` | Failure screenshot from a test run (captured by the screenshot-on-failure feature) |

The HTML report is generated to `reports/report.html` when running:
`pytest tests/ -v --html=reports/report.html --self-contained-html`
