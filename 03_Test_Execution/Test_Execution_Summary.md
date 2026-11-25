# Test Execution Summary

| Item | Detail |
| --- | --- |
| Application | Vehicle Traffic Violation and Fine Management System |
| Executor | [Member 3] |
| Cycle 1 | 17–18 November 2026, Build B1 |
| Fix | 19 November 2026, Build B2 |
| Retest | 20 November 2026, Build B2 |
| Window | 3 November 2026 – 21 November 2026 |

## Result

| | Cases | Pass | Fail |
| --- | ---: | ---: | ---: |
| Equivalence partitioning | 8 | 8 | 0 |
| Boundary value analysis | 8 | 8 | 0 |
| Decision table | 6 | 6 | 0 |
| State transition | 6 | 6 | 0 |
| **Final manual result** | **28** | **28** | **0** |

Cycle 1 was 21 Pass and 7 Fail. The same 7 cases passed on the retest. The log has one row per case.

## The seven failures were three defects

| Defect | What Build B1 did | Cases that failed | Retest |
| --- | --- | --- | --- |
| DEF-01 | Fined speed 60 | TC-BVA-01 | Pass |
| DEF-02 | Accepted no helmet for a Car | TC-EP-04, TC-DT-03 | Pass |
| DEF-03 | Did not add ₹200 after the due date | TC-BVA-06, TC-BVA-07, TC-DT-06, TC-ST-03 | Pass |

All three defects are Closed. The code in `05_Test_Automation/traffic_system/` is Build B2.

## Automated confirmation

`python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v` reports `Ran 30 tests` and `OK`. The console text is saved in `05_Test_Automation/test_run_output.txt`.
