# Test Execution Summary — VTFMS

| Item | Detail |
| --- | --- |
| Application | Vehicle Traffic Violation and Fine Management System |
| Baseline | `01_Test_Plan/Test_Plan.md` |
| Executor | [Member 3] |
| Cycle 1 | 17–18 November 2026, Build B1 |
| Fixes | 19 November 2026, Build B2 |
| Retest | 20 November 2026, Build B2 |
| Summary date | 21 November 2026 |
| Automation confirmation | 24 November 2026, Python 3.12.6, 92 passed, 0 failed |

Manual cases were executed against the specification and the local module. They were not executed against a deployed traffic-police system.

## Result

| Stage | Executed | Pass | Fail | Pass % |
| --- | ---: | ---: | ---: | ---: |
| Cycle 1 (17–18 Nov 2026) | 77 | 69 | 8 | 89.61% |
| Retest of the 8 failures (20 Nov 2026) | 8 | 8 | 0 | 100% |
| Final manual status | 77 | 77 | 0 | 100% |
| Automated unittest (24 Nov 2026) | 92 | 92 | 0 | 100% |

69 / 77 = 89.61%, rounded to two decimal places. The final manual percentage is 77 / 77 = 100%.

## By technique

| Technique | Cases | Cycle 1 Pass | Cycle 1 Fail | Final Pass |
| --- | ---: | ---: | ---: | ---: |
| Equivalence partitioning | 20 | 19 | 1 | 20 |
| Boundary value analysis | 24 | 19 | 5 | 24 |
| Decision table | 16 | 14 | 2 | 16 |
| State transition | 17 | 17 | 0 | 17 |
| Total | 77 | 69 | 8 | 77 |

The equivalence failure was TC-EP-11. The boundary failures were TC-BVA-02, TC-BVA-04, TC-BVA-06, TC-BVA-13, and TC-BVA-22. The decision-table failures were TC-DT-02 and TC-DT-08. Every state-transition case passed on Build B1.

## By module

| Module | Cases | Cycle 1 Pass | Cycle 1 Fail | Final Pass |
| --- | ---: | ---: | ---: | ---: |
| Registration | 6 | 5 | 1 | 6 |
| Licence | 4 | 4 | 0 | 4 |
| Challan recording | 12 | 10 | 2 | 12 |
| Fine calculation | 15 | 12 | 3 | 15 |
| Payment | 23 | 22 | 1 | 23 |
| Dispute | 11 | 10 | 1 | 11 |
| Reports | 6 | 6 | 0 | 6 |
| Total | 77 | 69 | 8 | 77 |

The module of each case is the module column in `02_Test_Case_Design/Test_Case_Index.md`.

## Cycle 1 dates

| Date | Cases | Pass | Fail |
| --- | --- | ---: | ---: |
| 17 Nov 2026 | 36 equivalence and decision-table cases | 33 | 3 |
| 18 Nov 2026 | 41 boundary and state-transition cases | 36 | 5 |

33 + 36 = 69 and 3 + 5 = 8.

## Defects found

| Defect | Cases that failed on B1 | Final status |
| --- | --- | --- |
| DEF-01 Speed-band off-by-one | TC-BVA-02, TC-BVA-04, TC-BVA-06 | Closed |
| DEF-02 Clearance blocked at exactly 5000 | TC-BVA-22 | Closed |
| DEF-03 No-helmet challan accepted for a non-two-wheeler | TC-EP-11, TC-DT-02 | Closed |
| DEF-04 Dispute accepted on day 16 | TC-BVA-13 | Closed |
| DEF-05 Early discount given for drunk driving | TC-DT-08 | Closed |

All five were fixed on 19 November 2026. The retest on 20 November 2026 passed. No defect was deferred.

## Automation

All 77 manual cases have an automated method. Fifteen further methods lock related rules (a missing licence, a dismissed prior, clearance unblocking, half-up rounding, and similar checks). The confirmation command was:

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

The saved output ends with `Ran 92 tests in 0.006s` and `OK`.

## Recommendation

Build B2 is ready for the faculty demonstration. The open risk is scope, not a failing rule: the module is not a live challan system.
