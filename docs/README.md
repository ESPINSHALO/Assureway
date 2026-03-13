# Documentation assets

Sample screenshots and terminal outputs from test and automation runs. Referenced from the main README.

| File | Description |
|------|-------------|
| `all-tests-output.png` | Terminal output for full suite (16 tests) |
| `regression-tests-output.png` | Terminal output for regression tests (12 tests) |
| `smoke-tests-output.png` | Terminal output for smoke tests (4 tests) |
| `html-tests-output.png` | HTML report generation output from a test run |
| `myntra-automation-output.png` | Output from standalone automation run (open_myntra_home.py) |
| `failure-test-output.png` | Failure screenshot from a test run (due to flaky tests; captured by the screenshot-on-failure feature) |

The HTML report is generated to `reports/report.html` when running:
`pytest tests/ -v --html=reports/report.html --self-contained-html`
